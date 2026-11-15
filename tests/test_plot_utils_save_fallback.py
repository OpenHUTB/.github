"""Regression tests for save_fig fallback behavior."""

import importlib.util
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from unittest import TestCase
from unittest.mock import Mock, patch


PLOT_UTILS_PATH = (
    Path(__file__).parents[1] / "docs" / "src" / "python" / "plot_utils.py"
)


def load_plot_utils():
    """Load plot_utils without requiring Matplotlib."""
    matplotlib = ModuleType("matplotlib")
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.rcParams = {}
    matplotlib.pyplot = pyplot
    with patch.dict(
        sys.modules,
        {
            "matplotlib": matplotlib,
            "matplotlib.pyplot": pyplot,
        },
    ):
        spec = importlib.util.spec_from_file_location(
            "plot_utils_save_under_test", PLOT_UTILS_PATH
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class SaveFigFallbackTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plot_utils = load_plot_utils()

    def test_failed_trimmer_saves_untrimmed_figure_and_replaces_stale_output(self):
        figure = Mock()
        figure_data = b"saved figure"

        def write_temporary_figure(path, **kwargs):
            Path(path).write_bytes(figure_data)

        figure.savefig.side_effect = write_temporary_figure

        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "figure.png"
            output.write_bytes(b"stale output")

            with patch.object(
                self.plot_utils.subprocess, "call", return_value=1
            ), self.assertLogs(self.plot_utils.__name__, level="WARNING") as logs:
                self.plot_utils.save_fig(figure, str(output))

            self.assertEqual(output.read_bytes(), figure_data)
            self.assertIn("untrimmed copy", logs.output[0])


if __name__ == "__main__":
    import unittest

    unittest.main()
