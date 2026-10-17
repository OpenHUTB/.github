"""Regression tests for the plotting helpers."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


PLOT_UTILS = (
    Path(__file__).resolve().parents[1] / "docs" / "src" / "python" / "plot_utils.py"
)


class FakeRcParams:
    """Small rcParams substitute that rejects unknown parameter names."""

    valid_keys = {
        "text.usetex",
        "figure.dpi",
        "font.size",
        "font.serif",
        "font.sans-serif",
        "font.monospace",
        "axes.labelsize",
        "axes.titlesize",
        "axes.linewidth",
        "legend.fontsize",
        "xtick.labelsize",
        "ytick.labelsize",
        "font.family",
    }

    def __init__(self):
        self.values = {}

    def update(self, params):
        invalid_keys = set(params) - self.valid_keys
        if invalid_keys:
            key = sorted(invalid_keys)[0]
            raise KeyError(f"{key} is not a valid rc parameter")
        self.values.update(params)


class FigureSetupTests(unittest.TestCase):
    def test_figure_setup_uses_valid_rcparams(self):
        rc_params = FakeRcParams()
        pyplot = types.ModuleType("matplotlib.pyplot")
        pyplot.rcParams = rc_params
        matplotlib = types.ModuleType("matplotlib")
        matplotlib.__path__ = []
        matplotlib.pyplot = pyplot

        with patch.dict(
            sys.modules,
            {"matplotlib": matplotlib, "matplotlib.pyplot": pyplot},
        ):
            spec = importlib.util.spec_from_file_location(
                "plot_utils_under_test", PLOT_UTILS
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.figure_setup()

        self.assertEqual(rc_params.values["font.size"], 10)
        self.assertNotIn("text.fontsize", rc_params.values)


if __name__ == "__main__":
    unittest.main()
