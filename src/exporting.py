from pathlib import Path
from typing import Tuple
# noinspection PyPep8Naming
from datetime import time as Time

from matplotlib import pyplot
from matplotlib.dates import DateFormatter
from src.util import paths
import seaborn


RESULTS_DIR = Path("../results")
paths.create_dir(RESULTS_DIR)

COLORS = {
    -1: "#FFFFFF",
    0: "#96bf33",
    1: "#E2571E",
    2: "#FF7F00",
    3: "#4B0082",
    4: "#00FF00",
    5: "#FFFF00",
    6: "#0000FF",
    7: "#FF0000",
    8: "#8B00FF",
    9: "#000000"
}


def save_stacked_plot(x, y1, y2, title: str):
    figure, axes = pyplot.subplots()
    axes.set_title(title)
    axes.set_xlabel("day")
    axes.set_ylabel("number of infectious")
    axes.set_ylim((0, 110))
    axes.stackplot(x, y1, y2)
    path = Path(RESULTS_DIR, title).with_suffix(".png")
    path_str = str(path)
    pyplot.savefig(path_str)


def save_plot(x, y, title: str):
    figure, axes = pyplot.subplots()
    axes.set_title(title)
    axes.set_xlabel("day")
    axes.set_ylabel("number of immigrants")
    axes.set_ylim((0, 300))
    axes.plot(x, y)
    axes.grid()
    path = Path(RESULTS_DIR, title).with_suffix(".png")
    path_str = str(path)
    pyplot.savefig(path_str)
