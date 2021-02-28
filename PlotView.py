# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    PlotView is summarized as PV in variable names.
"""


import tkinter as tk


# PV version as shown by git tag.
PV_VERSION = '0.1'
# Prevent the user from resizing the root window.
ROOT_RESIZABLE = False
# Root size (width x height) and posiiton relative to top left corner).
ROOT_SIZE_POS = '1280x720+0+0'


class App(tk.Tk):
    """"It defines the main window (root) of GUI."""
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.title('PlotView ' + PV_VERSION)
        self.geometry(ROOT_SIZE_POS)
        # Manage the size and position of root window.
        if ROOT_RESIZABLE:
            print('Warning: main window cannot be properly resized.')
        else:
            self.resizable(0, 0)


if __name__ == '__main__':
    app = App()
    app.mainloop()
