import math
import matplotlib.pyplot as plt
import os
import subprocess
import tempfile


def get_fig_size(fig_width_cm, fig_height_cm=None):
    """Convert dimensions in centimeters to a ``(width, height)`` tuple in inches.

    If no height is given, it is computed using the golden ratio.
    """
    if fig_height_cm is None:
        golden_ratio = (1 + math.sqrt(5))/2
        fig_height_cm = fig_width_cm / golden_ratio

    return (fig_width_cm / 2.54, fig_height_cm / 2.54)


"""
The following functions can be used by scripts to get the sizes of
the various elements of the figures.
"""


def label_size():
    """Size of axis labels
    """
    return 10


def font_size():
    """Size of all texts shown in plots
    """
    return 10


def ticks_size():
    """Size of axes' ticks
    """
    return 8


def axis_lw():
    """Line width of the axes
    """
    return 0.6


def plot_lw():
    """Line width of the plotted curves
    """
    return 1.5


def figure_setup(use_latex=True):
    """统一字体和线条尺寸，并配置是否使用 LaTeX 渲染文字。

    普通文字使用 font.size，坐标轴、图例和刻度可分别设置字号。
    """
    params = {'text.usetex': use_latex,
              'figure.dpi': 200,
              'font.size': font_size(),
              'axes.labelsize': label_size(),
              'axes.titlesize': font_size(),
              'axes.linewidth': axis_lw(),
              'legend.fontsize': font_size(),
              'xtick.labelsize': ticks_size(),
              'ytick.labelsize': ticks_size(),
              'font.family': 'serif'}
    plt.rcParams.update(params)


def save_fig(fig, file_name, fmt=None, dpi=300, tight=True):
    """Save a Matplotlib figure as EPS/PNG/PDF to the given path and trim it.
    """

    if not fmt:
        fmt = file_name.strip().split('.')[-1]

    if fmt not in ['eps', 'png', 'pdf']:
        raise ValueError('unsupported format: %s' % (fmt,))

    extension = '.%s' % (fmt,)
    if not file_name.endswith(extension):
        file_name += extension

    file_name = os.path.abspath(file_name)
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_name = tmp_file.name + extension

    # save figure
    if tight:
        fig.savefig(tmp_name, dpi=dpi, bbox_inches='tight')
    else:
        fig.savefig(tmp_name, dpi=dpi)

    # trim it
    if fmt == 'eps':
        subprocess.call('epstool --bbox --copy %s %s' %
                        (tmp_name, file_name), shell=True)
    elif fmt == 'png':
        subprocess.call('convert %s -trim %s' %
                        (tmp_name, file_name), shell=True)
    elif fmt == 'pdf':
        subprocess.call('pdfcrop %s %s' % (tmp_name, file_name), shell=True)
