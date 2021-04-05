# -*- coding: utf-8 -*-

"""PlotView GUI.
    It is the View in the Model View Controller pattern.
"""


import sys
import tkinter as tk
from tkinter import font


class Gui(tk.Tk):
    """"It defines the main window of GUI."""
    def __init__(self, application):
        """Initialize the main window.
        """
        super().__init__()
        self.app = application
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)
        self.window_setup()

    def window_setup(self):
        """Some basic setup is done on the GUI.
        Title is set.
        The size and location of the windows is set.
        The size cannot be changed at the moment beacause it is simpler.
        The default tkinter font is used with a lower size to pack more widgets.
        Constants:
        - PV_VERSION: string -> plot view version as shown by git tag.
        - ROOT_RESIZABLE: boolean -> prevents the user from resizing the root window.
        - ROOT_SIZE_POS: string -> Root size (width x height) and position relative to top left corner.
        - FONT_SIZE: integer -> size of font to be used for all widget texts.
        - PLOT_WIDTH: float -> width (in) of matplotlib figure.
        - PLOT_HEIGHT: float -> height (in) of matplotlib figure.
        """
        self.PV_VERSION = '0.2'
        self.ROOT_RESIZABLE = False
        self.ROOT_SIZE_POS = '1280x720+0+0'
        self.FONT_SIZE = 9
        self.PLOT_WIDTH = 9.0
        self.PLOT_HEIGHT = 6.68

        # WINDOW
        self.title('PlotView ' + self.PV_VERSION)
        # TODO: Exception if size > size of screen and quit.
        self.geometry(self.ROOT_SIZE_POS)
        # Manage the size and position of root window.
        if self.ROOT_RESIZABLE:
            print('Warning: the main window cannot be resized.')
        else:
            self.resizable(0, 0)
            # TODO: to be replaced by minsize() & maxsize() if I can handle
            # properly the change of size in the GUI.
        # FONT
        my_font = font.nametofont("TkDefaultFont")
        my_font.config(size=self.FONT_SIZE)
        # Make my_font applicable for all widgets including menus.
        self.option_add("*Font", my_font)

    def main(self):
        """Launch mainloop from App"""
        self.mainloop()

    def app_quit(self):
        """Quit the application"""
        # Destroy the root window.
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)
