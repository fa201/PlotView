# -*- coding: utf-8 -*-

"""PlotView GUI.
    It is the View in the Model View Controller pattern.
"""


import sys
import tkinter as tk
from tkinter import font
import webbrowser


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
        self.create_menus()
        self.create_status_bar()

    def window_setup(self):
        """Some basic setup is done on the GUI.

        Title is set.
        The size and location of the windows is set.
        The size cannot be changed at the moment because it is simpler.
        The default tkinter font is used with a lower size to pack more widgets.
        Constants:
        - PV_VERSION: string -> plot view version as shown by git tag.
        - WIN_RESIZABLE: boolean -> prevents the user from resizing the root window.
        - WIN_SIZE_POS: string -> window size (width x height) and position relative to top left corner.
        - FONT_SIZE: integer -> size of font to be used for all widget texts.
        - PLOT_WIDTH: float -> width (in) of matplotlib figure.
        - PLOT_HEIGHT: float -> height (in) of matplotlib figure.
        """
        self.PV_VERSION = '0.2'
        self.WIN_RESIZABLE = False
        self.WIN_SIZE_POS = '1280x720+0+0'
        self.FONT_SIZE = 9
        self.PLOT_WIDTH = 9.0
        self.PLOT_HEIGHT = 6.68

        # WINDOW
        self.title('PlotView ' + self.PV_VERSION)
        # TODO: Exception if size > size of screen and quit.
        self.geometry(self.WIN_SIZE_POS)
        # Manage the size and position of main window.
        if self.WIN_RESIZABLE:
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

    def app_quit(self):
        """Quit the application"""
        # Destroy the main window.
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)

    def create_menus(self):
        """Create the menus and sub-menus of the main GUI.
        Non-functional sub-menus are disabled.
        """
        # Main menu
        menu_main = tk.Menu(self)
        # Menu tear off is disabled.
        menu_file = tk.Menu(menu_main, tearoff='False')
        menu_pref = tk.Menu(menu_main, tearoff='False')
        menu_help = tk.Menu(menu_main, tearoff='False')
        # Add menu_file in menu_main
        menu_main.add_cascade(label='File', menu=menu_file)
        # TODO: customize picture format and size for export
        # menu_main.add_cascade(label='Preferences', menu=menu_pref)
        menu_main.add_cascade(label='Help', menu=menu_help)
        self.config(menu=menu_main)  # Link of main menu to root window
        # File Menu
        menu_file.add_command(label='Load session', state='disabled')
        menu_file.add_command(label='Save session as', state='disabled')
        menu_file.add_command(label='Export image', state='disabled')
        menu_file.add_command(label='Quit', command=self.app_quit)
        # Preferences Menu
        # menu_pref.add_command(label='Type of export image', state='disabled')
        # Help Menu
        menu_help.add_command(label='Help on PlotView', command=self.help_redirect)
        menu_help.add_command(label='Licence GPLv3', command=self.licence_redirect)
        menu_help.add_command(label='About', command=self.about_redirect)

    def help_redirect(self):
        """Plotview wiki is shown in web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/wiki/Help')
        self.set_status('The PlotView wiki page is shown in your web browser.')

    def licence_redirect(self):
        """PlotView licence is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/blob/master/LICENSE')
        self.set_status('The page of GPL3 licence is shown in your web browser.')

    def about_redirect(self):
        """PlotView repository is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')
        self.set_status('The PlotView repository on github was opened in your web browser.')

    def create_status_bar(self):
        """A status bar is created à the bottom.
        It shows text message through 'set_status' ."""
        self.status_frame = tk.Frame(self)
        # self.status_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S) A garder ?
        # The status frame should extend on all width of the App window
        self.status_frame.pack(expand=True, fill=tk.X, side=tk.BOTTOM)
        # The status is initialised with empty message left aligned.
        self.status = tk.Label(self.status_frame, text=' ', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        # The label shoul expand on the total width
        self.status.pack(fill=tk.BOTH, expand=True)

    def set_status(self, string):
        """Update the status bar message."""
        # Add 1 space on the left to give more room relative to the window left border
        self.status.config(text=' '+string)
