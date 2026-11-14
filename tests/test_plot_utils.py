"""Regression tests for the figure-saving helper."""

import importlib.util
import subprocess
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

    def test_png_path_with_spaces_is_preserved_and_failures_are_raised(self):
        figure = Mock()
        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "target with space.png"
            failure = subprocess.CalledProcessError(1, "convert")
            with patch.object(
                self.plot_utils.subprocess,
                "check_call",
                side_effect=failure,
            ) as check_call:
                with self.assertRaises(subprocess.CalledProcessError):
                    self.plot_utils.save_fig(figure, str(output))

            check_call.assert_called_once_with([
                "convert", ANY, "-trim", str(output.resolve())
            ])


if __name__ == "__main__":
    import unittest

    unittest.main()
