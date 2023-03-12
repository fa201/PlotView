# -*- coding: utf-8 -*-

try:
    # from collections import OrderedDict
    # import configparser
    # import os
    # import pandas as pd
    import tkinter as tk
    # from tkinter import filedialog
    import tkinter.ttk as ttk
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')
    # TODO how to use same exception for all imports. Class?


class StatusBar():
    """Manage the status bar showing messages.

    Help: https://stackoverflow.com/questions/73704408/tkinter-pack-add-space-beteen-elements

    Method:
    - set_status: update the status bar with a message.
    """

    def __init__(self, parent):
        self.parent = parent
        # TODO A frame is created to hold the progress bar and status bar.
        self.status_frame = ttk.Frame(self.parent)
        # The status frame should extend on all width of the main window.
        self.status_frame.pack(expand=False, fill=tk.X, side=tk.BOTTOM)
        # The status is initialized with left aligned.
        self.status = ttk.Label(self.status_frame,
                                text='',
                                relief=tk.SUNKEN,
                                anchor=tk.W
                                )
        # The label should expand on the total available space.
        self.status.pack(fill=tk.BOTH, expand=False)
        self.set_status('Ready.')

    def set_status(self, message):
        """ Update the status bar message.

        A space is added on the left to give more room relative to the window border.
        """
        self.status.config(text=''.join([' ', message]))
