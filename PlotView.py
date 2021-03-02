# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    PlotView is summarized as PV in variable names.
"""


import tkinter as tk
from tkinter import font
import tkinter.messagebox
import sys
import webbrowser


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
        self.create_menus()
        # Allows root window to be closed by the closing icon
        self.protocol('WM_DELETE_WINDOW', self.app_quit)

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

    def create_menus(self):
        """Create the menus and sub-menus of the main GUI"""
        # Main menu
        menu_main = tk.Menu(self)
        menu_file = tk.Menu(menu_main, tearoff='False')  # Disable tear off menu.
        menu_pref = tk.Menu(menu_main, tearoff='False')
        menu_help = tk.Menu(menu_main, tearoff='False')
        menu_main.add_cascade(label='File', menu=menu_file)  # Add menu_file in menu_main
        menu_main.add_cascade(label='Preferences', menu=menu_pref)
        menu_main.add_cascade(label='Help', menu=menu_help)
        self.config(menu=menu_main)  # Link of main menu to root window
        # File Menu
        menu_file.add_command(label='Load session', state='disabled')
        menu_file.add_command(label='Save session as', state='disabled')
        menu_file.add_command(label='Export image', state='disabled')
        menu_file.add_command(label='Quit', command=self.app_quit)
        # Preferences Menu
        menu_pref.add_command(label='Type of export image', state='disabled')
        # Help Menu
        menu_help.add_command(label='Help on PlotView', state='disabled')
        menu_help.add_command(label='Licence GPLv3', command=self.licence_redirect)
        menu_help.add_command(label='About', command=self.about_redirect)

    def licence_redirect(self):
        """PlotView licence is shown in the web browser."""
        print('The PlotView licence is shown in your web browser.')
        # TODO: convert this message to status bar message
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/blob/master/LICENSE')

    def about_redirect(self):
        """PlotView repository is shown in the web browser."""
        print('The PlotView repository on github was opened in your web browser.')
        # TODO: convert this message to status bar message
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')

    def app_quit(self):
        # print('Enter app_quit()')  # Only for debug.
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)


if __name__ == '__main__':
    app = App()
    app.mainloop()
