# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    PlotView is summarized as PV in variable names.
"""


import tkinter as tk
from tkinter import font
import sys


# Constants
# PV version as shown by git tag.
PV_VERSION = '0.1'
# Prevent the user from resizing the root window.
ROOT_RESIZABLE = False
# Root size (width x height) and posiiton relative to top left corner).
ROOT_SIZE_POS = '1280x720+0+0'
# Font size applicable for all GUI texts
FONT_SIZE = 9


class App(tk.Tk):
    """"It defines the main window (root) of GUI."""
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.root_setup()
        self.font_setup()
        # Allows root window to be closed by the closing icon
        self.protocol('WM_DELETE_WINDOW', self.root_quit)

    def root_setup(self):
        self.title('PlotView ' + PV_VERSION)
        self.geometry(ROOT_SIZE_POS)
        # Manage the size and position of root window.
        if ROOT_RESIZABLE:
            print('Warning: main window cannot be properly resized.')
        else:
            self.resizable(0, 0)
            # TODO: to be replaced by minsize() & maxsize() if I can handle
            # properly the change of size in the GUI.

    def font_setup(self):
        # Customized font based on TkDefaultFont
        my_font = font.nametofont("TkDefaultFont")
        # Font size reduced to have a tighter layout
        my_font.config(size=FONT_SIZE)
        # Make my_font applicable for all widgets including menus.
        self.option_add("*Font", my_font)

    def root_quit(self):
        print('Enter root_quit()')
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)


if __name__ == '__main__':
    app = App()
    app.mainloop()
