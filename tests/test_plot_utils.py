import importlib.util
import shlex
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


PLOT_UTILS_PATH = (Path(__file__).parents[1] / "docs" / "src" / "python" /
                   "plot_utils.py")


def load_plot_utils():
    matplotlib = types.ModuleType("matplotlib")
    pyplot = types.ModuleType("matplotlib.pyplot")
    matplotlib.pyplot = pyplot
    spec = importlib.util.spec_from_file_location("plot_utils_under_test",
                                                  PLOT_UTILS_PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {
            "matplotlib": matplotlib,
            "matplotlib.pyplot": pyplot,
    }):
        spec.loader.exec_module(module)
    return module


class FakeFigure:
    def __init__(self):
        self.saved_path = None

    def savefig(self, path, **kwargs):
        self.saved_path = Path(path)
        self.saved_path.write_bytes(b"figure")


def fake_trim(command, shell):
    parts = shlex.split(command)
    shutil.copyfile(parts[1], parts[-1])
    return 0


class SaveFigTests(unittest.TestCase):
    def test_png_output_is_created_and_temporary_file_is_removed(self):
        plot_utils = load_plot_utils()
        figure = FakeFigure()

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "figure.png"
            try:
                with patch.object(plot_utils.subprocess, "call",
                                  side_effect=fake_trim) as trim:
                    plot_utils.save_fig(figure, str(output), fmt="png")

                self.assertTrue(output.exists())
                self.assertIsNotNone(figure.saved_path)
                self.assertFalse(figure.saved_path.exists())
                trim.assert_called_once()
            finally:
                if figure.saved_path and figure.saved_path.exists():
                    figure.saved_path.unlink()


if __name__ == "__main__":
    unittest.main()
