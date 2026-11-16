"""Regression tests for the figure-saving helper."""

import importlib.util
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from unittest import TestCase
from unittest.mock import ANY, Mock, patch


PLOT_UTILS_PATH = Path(__file__).parents[1] / "docs" / "src" / "python" / "plot_utils.py"


def load_plot_utils():
    """Load plot_utils without requiring matplotlib for this unit test."""
    matplotlib = ModuleType("matplotlib")
    pyplot = ModuleType("matplotlib.pyplot")
    matplotlib.pyplot = pyplot
    with patch.dict(sys.modules, {
        "matplotlib": matplotlib,
        "matplotlib.pyplot": pyplot,
    }):
        spec = importlib.util.spec_from_file_location("plot_utils_under_test", PLOT_UTILS_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class SaveFigTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plot_utils = load_plot_utils()

    def test_png_path_with_spaces_is_preserved_when_trimmer_fails(self):
        figure = Mock()
        figure_data = b"saved figure"

        def write_temporary_figure(path, **kwargs):
            Path(path).write_bytes(figure_data)

        figure.savefig.side_effect = write_temporary_figure

        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "target with space.png"
            with patch.object(
                self.plot_utils.subprocess,
                "call",
                return_value=1,
            ) as call:
                self.plot_utils.save_fig(figure, str(output))

            call.assert_called_once_with([
                "convert", ANY, "-trim", str(output.resolve())
            ])
            self.assertEqual(output.read_bytes(), figure_data)


if __name__ == "__main__":
    import unittest

    unittest.main()
