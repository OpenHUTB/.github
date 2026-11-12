"""Regression tests for plot_utils.get_fig_size."""

import importlib.util
import math
import sys
from pathlib import Path
from types import ModuleType
from unittest import TestCase
from unittest.mock import patch


PLOT_UTILS_PATH = (
    Path(__file__).parents[1] / "docs" / "src" / "python" / "plot_utils.py"
)


def load_plot_utils():
    """Load plot_utils without requiring Matplotlib for this size-only test."""
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
            "plot_utils_under_test", PLOT_UTILS_PATH
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class GetFigSizeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plot_utils = load_plot_utils()

    def test_explicit_size_returns_inches_as_tuple(self):
        size = self.plot_utils.get_fig_size(10, 5)

        self.assertIsInstance(size, tuple)
        self.assertEqual(size, (10 / 2.54, 5 / 2.54))

    def test_missing_height_uses_golden_ratio(self):
        size = self.plot_utils.get_fig_size(10)
        expected_height = 10 / ((1 + math.sqrt(5)) / 2)

        self.assertEqual(size, (10 / 2.54, expected_height / 2.54))


class FigureSetupTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plot_utils = load_plot_utils()

    def test_can_disable_latex_without_clearing_font_families(self):
        self.plot_utils.plt.rcParams.clear()

        self.plot_utils.figure_setup(use_latex=False)

        params = self.plot_utils.plt.rcParams
        self.assertFalse(params["text.usetex"])
        self.assertNotIn("font.serif", params)
        self.assertNotIn("font.sans-serif", params)
        self.assertNotIn("font.monospace", params)


if __name__ == "__main__":
    import unittest

    unittest.main()
