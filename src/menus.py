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
    """All menus of GUI"""

    def __init__(self, parent):
        self.parent = parent
        self.menu_main = tk.Menu(self.parent)
        # Menu tear off is disabled.
        self.menu_file = tk.Menu(self.menu_main, tearoff='False')
        self.menu_pref = tk.Menu(self.menu_main, tearoff='False')
        self.menu_help = tk.Menu(self.menu_main, tearoff='False')
        # Add menu_file in menu_main
        self.menu_main.add_cascade(label='File', menu=self.menu_file)
        self.menu_main.add_cascade(label='Help', menu=self.menu_help)
        # Link of main menu to root window
        self.parent.config(menu=self.menu_main)
        # File Menu
        self.menu_file.add_command(
            label='Load session', command=self.load_session)
        self.menu_file.add_command(
            label='Save session', command=self.save_session)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Quit', command=self.parent.app_quit)
        # Help Menu
        self.menu_help.add_command(
            label='Help files', command=self.help_message)
        self.menu_help.add_command(
            label='Licence', command=self.licence_message)
        self.menu_help.add_separator()
        self.menu_help.add_command(label='About', command=self.about_redirect)

    def help_message(self):
        """ Give directions to help files."""
        m1 = 'Help is available in the "test" folder with the "index.html" file. '
        m2 = 'In case you have not downloaded this folder, it is available at:\n'
        m3 = 'https://github.com/fa201/PlotView'
        msg.showinfo('Help', ''.join([m1, m2, m3]))

    def licence_message(self):
        """ Give directions to the licence file."""
        m1 = 'PlotView is licensed under GNU GPL-3.0. '
        m2 = 'In case you have not downloaded the "LICENSE" file, it is available at:\n'
        m3 = 'https://github.com/fa201/PlotView'
        msg.showinfo('License', ''.join([m1, m2, m3]))

    def about_redirect(self):
        """ PlotView repository is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')
        self.parent.status_bar.set_status(
            'The PlotView repository on github was opened in your web browser.')

    def save_session(self):
        pass

    def load_session(self):
        pass
