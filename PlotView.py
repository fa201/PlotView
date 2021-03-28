# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    PlotView is summarized as PV in variable names.
"""


import pandas as pd
import sys
import tkinter as tk
from tkinter import font
import webbrowser


class App(tk.Tk):
    """"It defines the main window of GUI."""
    def __init__(self):
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
        self.constant_setup()
        self.root_setup()
        self.create_menus()
        self.create_status_bar()
        # After launching App the status should be Ready.
        self.set_status('Ready.')
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)

    def constant_setup(self):
        """Define constants used in PV

        Constants:
        - PV_VERSION: float -> PV version as shown by git tag.
        - ROOT_RESIZABLE: boolean -> prevents the user from resizing the root window.
        - ROOT_SIZE_POS: string -> Root size (width x height) and position relative to top left corner.
        - FONT_SIZE: integer -> size of font to be used for all widget texts.
        """
        self.PV_VERSION = '0.2'
        self.ROOT_RESIZABLE = False
        self.ROOT_SIZE_POS = '1280x720+0+0'
        self.FONT_SIZE = 9


    def root_setup(self):
        """Some basic setup is done on the GUI.

        Title is set.
        The size and location of the windows is set.
        The size cannot be changed at the moment beacause it is simpler.
        The default tkinter font is used with a lower size to pack more widgets.
        """
        # WINDOW
        self.title('PlotView ' + self.PV_VERSION)
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

    def create_menus(self):
        """Create the menus and sub-menus of the main GUI.

        Non-functional sub-menus are disabled.
        """
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
        menu_help.add_command(label='Help on PlotView', command=self.help_redirect)
        menu_help.add_command(label='Licence GPLv3', command=self.licence_redirect)
        menu_help.add_command(label='About', command=self.about_redirect)

    def help_redirect(self):
        """Plotview wiki is shown in web browser."""
        self.set_status('The PlotView wiki page is shown in your web browser.')
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/wiki/Help')

    def licence_redirect(self):
        """PlotView licence is shown in the web browser."""
        self.set_status('The page of GPL3 licence is shown in your web browser.')
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/blob/master/LICENSE')

    def about_redirect(self):
        """PlotView repository is shown in the web browser."""
        self.set_status('The PlotView repository on github was opened in your web browser.')
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')

    def app_quit(self):
        """Quit the App and free the stack."""
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)

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


class Curve:
    """Contains all the data relative to a curve.

    Class attribute 'count' is used to describe the curve ID.
    The default plotting parameters are those below (user can change them).
    Attributes:
        - id: integer -> curve ID (cannot be changed by the user)
        - name: string -> curve name as shown in the plot legend
        - file: string -> path to CSV file
        - data: dataframe -> contains (X,Y) points to be plotted
        - data_type: dictionary -> contains X header and Y header
        - visibility: boolean -> flag to show the curve in the plot or not
        - color: string -> color of the curve line
        - width: float -> width of the curve line
        - style: string -> style of the curve line
        - marker: string -> line marker (symbol) for the curve
        - marker_size: float -> size of line marker for the curve
    Methods:
        - method to read the CSV file
        - method plot the curve
    """
    # Count the number of curves created
    count = 1

    def __init__(self, file):
        # Curve ID: must be unique.
        # '0' is added from 1 to 9 to keep the order when sorted as text.
        if Curve.count < 10:
            # Format integrer to string to avoid this later on.
            self.id = '0' + str(Curve.count)
        else:
            self.id = str(Curve.count)
        # Curve ID is shown to avoid confusion until the relevant name is defined.
        self.name = 'Curve_' + self.id
        self.file = file
        self.data = self.read_file(file)
        # TODO: handle this with a function and exceptions if no column or 1 column
        self.data_type = {'x_type': self.data.columns[0], 'y_type': self.data.columns[1]}
        #
        self.visibility = True
        self.color = 'black'
        # TODO: what are the limits of width?
        self.width = 1.0
        # TODO: what are the options?
        self.style = 'solid'
        # TODO: what are the options?
        self.marker = 'o'
        # TODO: what are the limits?
        self.marker_size = 1.0
        Curve.count += 1

    def read_file(self, ):
        """Read the curve CSV file.

        It is necessary to convert data to float in 'read_csv' in order to plot.
        Requirements on the file format:
                - delete unused data and headers: header should be on the first line
                - rename column headers if necessary
                - only 2 columns of data
                - strip unwanted spaces
                - make sure that comma is the delimiter
                - decimal character is the point '.'
        """
        df = pd.read_csv(self.file, delimiter=',', dtype=float)
        message = 'Curve ID {0} - size of data (lines, colums): {1}'
        # TODO: check that the status bar is updated.
        app.set_status(message.format(self.id, df.shape))
        return df


if __name__ == '__main__':
    # Create the main GUI
    app = App()
    app.mainloop()
