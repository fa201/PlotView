# -*- coding: utf-8 -*-

""" PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    PlotView is summarized as PV in variable names.
"""


class Model:
    """ Define some default values for directories or files

        The working directory is supposed to contain several CSV curve files to plot.
        The goal is to avoid repeating navigation to the same directory for data.
        It is supposed to be changed once or a few times per PlotView session.

        The working file shows the current curve CSV file used, once the file is loaded.

        Variables:
        - work_dir: string -> complete path to the working directory
        - work_dir_txt: string -> short path showing the end of 'work_dir'
    """
    def __init__(self):
        pass
