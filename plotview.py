# -*- coding: utf-8 -*-

""" PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    Licence: GNU GPL-3.0
    PlotView is summarized as PV in variable names.
"""


try:
    # from collections import OrderedDict
    # import configparser
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    # from matplotlib.ticker import MaxNLocator
    # import os
    # import pandas as pd
    import sys
    import tkinter as tk
    from tkinter import font
    # from tkinter import messagebox as msg
    # from tkinter import filedialog
    import tkinter.ttk as ttk
    # import webbrowser

    from src.menus import Menus
    from src.status_bar import StatusBar
    from src.create_curve_tab import CreateCurveTab
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')
    # TODO how to use same exception for all imports. Class?


"""TODO Gets and prints the spreadsheet's header columns

Args:
    file_loc (str): The file location of the spreadsheet
    print_cols (bool): A flag used to print the columns to the console
        (default is False)

Attributes:
    zjbnzjbn
    

Returns:
    list: a list of strings representing the header columns
    
Raises:
    jnaemrj eaj
"""


class Application(tk.Tk):
    """"It defines the main window of GUI."""

    def __init__(self):
        """ Initialize the main window.

        The window is launched with a size of 1280 x 720 but it can be resized.
        The matplotlib area is defined 16 x 12 in which is bigger than the available space.
        Yet it is not a problem because it is handled by tk window manager.

        Constants:
        - PV_VERSION: string -> plot view version as shown by git tag.
        - WIN_RESIZABLE: boolean -> prevents the user from resizing the root window.
        - WIN_SIZE_POS: string -> window size (width x height) and position relative
                                    to top left corner.
        - FONT_SIZE: integer -> size of font to be used for all widget texts.
        - PLOT_WIDTH: float -> width (in) of matplotlib figure.
        - PLOT_HEIGHT: float -> height (in) of matplotlib figure.

        Variables: to be completed

        Methods: to be completed
        """
        super().__init__()
        # Version is positioned here to be easy to find.
        self.PV_VERSION = '1.9'
        self.define_window_parameters()
        self.setup_GUI_look()
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)
        self.menus = Menus(self)
        self.status_bar = StatusBar(self)
        self.create_main_panels()
        self.create_curve_tab = CreateCurveTab(self)

    def define_window_parameters(self):
        """Define main window parameter: title, size, position."""
        self.title(' '.join(['PlotView', self.PV_VERSION]))
        # Window size should be OK for most cases. Window positioned at top left corner.
        self.WIN_SIZE_POS = '1280x780+0+0'
        self.geometry(self.WIN_SIZE_POS)

    def setup_GUI_look(self):
        """Define ttk style, font, button sizes 

        ttk style
            - Do not work for TEntry, TCombobox
            - Optional themes: default, clam, alt, classic

        Font:
            - A font is used with a lower size to pack more widgets and fixed spacing.
            - Help:
                https://stackoverflow.com/questions/31918073/tkinter-how-to-set-font-for-text
                https://stackoverflow.com/questions/15462647/how-to-modify-the-default-font-in-tkinter

        Define 3 sizes of TButtons to be used for most buttons: 4, 6, 9
        """
        self.my_style = ttk.Style()
        self.my_style.theme_use('alt')

        # Buttons size. Help https://tkdocs.com/shipman/ttk-style-layer.html
        # TODO https://stackoverflow.com/questions/49230658/tkinter-how-to-apply-customized-ttk-stylename-that-is-defined-in-one-class-to-o
        """
        self.my_style.configure('w4.TButton', width=4)
        self.my_style.configure('w6.TButton', width=6)
        self.my_style.configure('w9.TButton', width=9)
        """

        # Fonts
        self.FONT_SIZE = 9
        my_font = tk.font.nametofont('TkDefaultFont')
        my_font.configure(size=self.FONT_SIZE)
        # Apply font change to all widgets created from now on.
        self.option_add("*Font", my_font)

        # Parameters for widgets on RH tool panel.
        # Padding for all containers to uniformize the look
        # self.CONTAINER_PADX = 10
        # self.CONTAINER_PADY = 6.5
        # Padding for all widgets inside a container
        # self.WIDGET_PADX = 2.5
        # self.WIDGET_PADY = 2.5

        # Number of decimals for rounding operation
        self.ROUND = 5

    def create_main_panels(self):
        """Create 2 panels containing the matplotlib and tabs widgets

        On the right, a frame 'tool_frame' holds the notebook showing curve related tabs. It needs to be created before the matplotlib frame.

        On the left, a frame 'mat_frame' embeds the matplotlib plot and tool bar.
        This frame contains the canvas holding the matplotlib figure and tool bar.
        The size of the figure needs to large to fill all the space on large screen.

        Help on layout: https://stackoverflow.com/questions/29432683/resizing-a-matplotlib-plot-in-a-tkinter-toplevel

        Attributes:
            PLOT_WIDTH: width of matplotlib plot in inches.
            PLOT_HEIGHT: height of matplotlib plot in inches.
            fig: matplotlib figure holding the unique plot (1 axes)
        """
        # CREATE RH TOOL PANEL
        self.tool_frame = ttk.Frame(self)
        self.tool_frame.pack(expand=False, fill=tk.BOTH, side=tk.RIGHT)
        self.tool_notebook = ttk.Notebook(self.tool_frame)
        self.tool_notebook.pack(expand=True, fill=tk.BOTH)
        # CREATE LH MATPLOTLIB PANEL
        self.PLOT_WIDTH = 20
        self.PLOT_HEIGHT = 12
        self.fig = plt.Figure(figsize=(self.PLOT_WIDTH, self.PLOT_HEIGHT))
        self.ax = self.fig.add_subplot(111)
        # plot_fig_color is initialized here but the value will be updated based on radiobutton state in plot curve tab.
        self.plot_fig_color = 'white_bg'
        self.mat_frame = ttk.Frame(self)
        self.mat_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mat_frame)
        self.canvas.draw()  # Draw the canvas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.mat_frame)
        # draw() shows a bug with matplotlib 3.5 and it is replaced by update()
        self.toolbar.update()  # Show the tool bar
        self.canvas.get_tk_widget().pack()

    def app_quit(self):
        """ Quit the application and free the stack."""
        self.destroy()
        sys.exit()


if __name__ == '__main__':
    app = Application()
    """
    # Show the screen dimensions at start-up.
    screen_height = app.winfo_screenheight()
    screen_width = app.winfo_width()
    print('Screen height', screen_height)
    print('Screen width', screen_width)
    """
    # Define the min size for the window. It should be enough even for old screens.
    app.minsize(800, 610)
    # Launch the GUI mainloop which should always be the last instruction!
    app.mainloop()
