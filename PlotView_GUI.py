# -*- coding: utf-8 -*-

"""PlotView GUI.
    It is the View in the Model View Controller pattern.
"""


import sys
import tkinter as tk


class Gui(tk.Tk):
    """"It defines the main window of GUI."""
    def __init__(self, app):
        """Initialize the main window.

        The following actions are done:
            1/ Set some constants
            2/ Set the main GUI up
            3/ Set the font up for all texts in widgets
            4/ Create the GUI menus at the top
            5/ Create the status bar at the bottom
            6/ Set the status bar to 'Ready'
        """
        super().__init__()
        self.app = app
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)

    def main(self):
        """Launch mainloop from App"""
        self.mainloop()

    def app_quit(self):
        """Quit the application"""
        # Destroy the root window.
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)
