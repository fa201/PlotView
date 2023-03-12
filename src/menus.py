# -*- coding: utf-8 -*-

try:
    # from collections import OrderedDict
    # import configparser
    # import os
    # import pandas as pd
    import tkinter as tk
    from tkinter import font
    from tkinter import messagebox as msg
    # from tkinter import filedialog
    import tkinter.ttk as ttk
    import webbrowser
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')
    # TODO how to use same exception for all imports. Class?


class Menus():
    """All menus of GUI. TODO use constant for messages ?

    Menu tear-off is disabled as it is for modern applications.
    """

    def __init__(self, parent):
        self.parent = parent

        self.menu_main = tk.Menu(self.parent)
        self.menu_file = tk.Menu(self.menu_main, tearoff='False')
        # TODO self.menu_pref = tk.Menu(self.menu_main, tearoff='False')
        self.menu_help = tk.Menu(self.menu_main, tearoff='False')

        # File Menu
        self.menu_main.add_cascade(label='File', menu=self.menu_file)
        self.menu_file.add_command(
            label='Load session', command=self.load_session)
        self.menu_file.add_command(
            label='Save session', command=self.save_session)
        self.menu_file.add_separator()
        self.menu_file.add_command(
            label='Quit', command=self.parent.quit_application)

        # Help Menu
        self.menu_main.add_cascade(label='Help', menu=self.menu_help)
        self.menu_help.add_command(
            label='Help files', command=self.show_help_dialog)
        self.menu_help.add_command(
            label='Licence', command=self.show_licence_dialog)
        self.menu_help.add_separator()
        self.menu_help.add_command(
            label='About', command=self.show_about_redirect_to_repository)

        # Addition of main menu to application window
        self.parent.config(menu=self.menu_main)

    def show_help_dialog(self):
        """ Give directions to help files."""
        m1 = 'Help is available in the "help" folder with the file "index.html".\n'
        m2 = 'In case you do not have this folder, please visit the Github repository: menu HELP > ABOUT.'
        msg.showinfo('Help', ''.join([m1, m2]))

    def show_licence_dialog(self):
        """ Give directions to the licence file."""
        m1 = 'PlotView is licensed under GNU GPL-3.0.\n'
        m2 = 'The "LICENSE" file is available in the same folder as "plotview.py".\n'
        m3 = 'In case you do not have this file, please visit the Github repository: menu HELP > ABOUT.'
        msg.showinfo('License', ''.join([m1, m2, m3]))

    def show_about_redirect_to_repository(self):
        """ PlotView repository is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')
        self.parent.status_bar.set_status(
            'The PlotView repository on Github was opened in your web browser.')

    def save_session(self):
        pass

    def load_session(self):
        pass
