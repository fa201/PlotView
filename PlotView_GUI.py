# -*- coding: utf-8 -*-

"""PlotView GUI.
    It is the View in the Model View Controller pattern.
"""

try:
    import sys
    import tkinter as tk
    from tkinter import font
    from tkinter import messagebox as msg
    from tkinter import filedialog
    from tkinter import ttk
    import webbrowser
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
except ModuleNotFoundError as e:
        print('The necessary Python packages are not installed.\n' + str(e))
        print('Please check the required packages and their versions at https://github.com/fa201/PlotView.')


class Gui(tk.Tk):
    """"It defines the main window of GUI."""
    def __init__(self, application):
        """Initialize the main window.

        Constants:
        - PV_VERSION: string -> plot view version as shown by git tag.
        - WIN_RESIZABLE: boolean -> prevents the user from resizing the root window.
        - WIN_SIZE_POS: string -> window size (width x height) and position relative to top left corner.
        - FONT_SIZE: integer -> size of font to be used for all widget texts.
        - PLOT_WIDTH: float -> width (in) of matplotlib figure.
        - PLOT_HEIGHT: float -> height (in) of matplotlib figure.
        - MAX_STR_CREATE_CURVE: int -> number of caracters to be displayed to show the working directory.

        Variables:
        - work_dir_txt: string -> end of directory path showing working directory.
        """
        super().__init__()

        # ATTRIBUTES
        # Link to Application instance (Controller)
        self.app = application
        # Main window parameters.
        self.PV_VERSION = '0.2'
        self.WIN_RESIZABLE = False
        self.WIN_SIZE_POS = '1280x720+0+0'
        self.FONT_SIZE = 9
        # Matplotlib parameters.
        self.PLOT_WIDTH = 9.0
        self.PLOT_HEIGHT = 6.68
        # Parameters for widgets on RH tool panel.
        # Padding for all containers to uniformize the look
        self.CONTAINER_PADX = 7
        self.CONTAINER_PADY = 7
        # Padding for all widgets inside a container
        self.WIDGET_PADX = 2
        self.WIDGET_PADY = 2
        # Max length of string showed by 'Create curve' labels
        self.MAX_STR_CREATE_CURVE = 32

        # Working directory variables.
        # 'work_dir_set' defines the directory for the CSV filedialog.
        self.work_dir_txt = tk.StringVar(self)
        self.work_dir_txt.set('___________________________________')

        # Path to CSV file
        # TODO: a changer et à utiliser Curve ?
        # work_file define the CSV file path
        self.work_file_txt = tk.StringVar(self)
        self.work_file_txt.set('___________________________________')
        # Displayed working file path (only last characters.)
        #self.work_file_txt.set(self.work_file[-35:-1])

        # METHODS
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)
        self.window_setup()
        self.create_menus()
        self.create_plot_area()
        self.create_notebook()
        self.tab_curve()

    def window_setup(self):
        """Some basic setup is done on the GUI.

        Title is set.
        The size and location of the windows is set.
        The size cannot be changed at the moment because it is simpler.
        A font is used with a lower size to pack more widgets and fixed sapcing.
        A status bar is created at the bottom. It shows text message through 'set_status'.
        """
        # WINDOW
        self.title('PlotView ' + self.PV_VERSION)
        # TODO: Exception if size > size of screen and quit.
        self.geometry(self.WIN_SIZE_POS)
        if self.WIN_RESIZABLE:
            print('Warning: the main window cannot be resized.')
        else:
            self.resizable(0, 0)
            # TODO: to be replaced by minsize() & maxsize() if I can handle
            # properly the change of size in the GUI.

        # FONT
        # https://stackoverflow.com/questions/31918073/tkinter-how-to-set-font-for-text
        my_font = font.Font(family='TkFixedFont', size=self.FONT_SIZE)
        self.option_add("*Font", my_font)

        # STATUS BAR
        self.status_frame = tk.Frame(self)
        # self.status_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S) A garder ?
        # The status frame should extend on all width of the main window.
        self.status_frame.pack(expand=True, fill=tk.X, side=tk.BOTTOM)
        # The status is initialized with empty message left aligned.
        self.status = tk.Label(self.status_frame, text=' ', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        # The label shoul expand on the total window width.
        self.status.pack(fill=tk.BOTH, expand=True)

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
        # menu_pref = tk.Menu(menu_main, tearoff='False')
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

    def set_status(self, string):
        """Update the status bar message."""
        # Add 1 space on the left to give more room relative to the window left border
        self.status.config(text=' '+string)

    def create_plot_area(self):
        # TODO: https://stackoverflow.com/questions/29432683/resizing-a-matplotlib-plot-in-a-tkinter-toplevel
        self.fig = plt.Figure(figsize=(self.PLOT_WIDTH, self.PLOT_HEIGHT))
        self.ax = self.fig.add_subplot(111)
        self.mat_frame = tk.Frame(self)
        #mat_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.mat_frame.pack(expand=False, side=tk.LEFT)
        # Creates a drawing area to put the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mat_frame)
        self.canvas.draw()
        # Creates the Matplotlib navigation tool bar for figures.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.mat_frame)
        self.toolbar.draw()
        self.canvas.get_tk_widget().pack()

    def create_notebook(self):
        """Notebook on RH panel containing all the tool tabs."""
        # Frame for RH panel. It contains the ttk.notebook.
        self.tool_frame = tk.Frame(self)
        self.tool_frame.pack(expand=True, fill=tk.BOTH)
        # Notebook
        self.tool_notebook = ttk.Notebook(self.tool_frame)
        self.tool_notebook.pack(expand=True, fill=tk.BOTH)

    def tab_curve(self):
        """First tab managing curve creation."""
        # Create curve tab
        self.curve_tab = ttk.Frame(self.tool_notebook)

        # Create curve panel
        self.curve_frame = tk.LabelFrame(self.curve_tab, text='Create curve', bg='green')
        self.curve_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY)

        # Working directory widgets
        tk.Button(self.curve_frame, text='Choose directory',
                command=self.choose_dir, width=12).grid(
                row=0, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        tk.Label(self.curve_frame, textvariable=self.work_dir_txt).grid(
                row=0, column=1, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.W)

        # CSV file widgets
        tk.Button(self.curve_frame, text='Choose CSV file',
                command=self.choose_file, width=12).grid(
                row=1, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        tk.Label(self.curve_frame, textvariable=self.work_file_txt).grid(
                row=1, column=1, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.W)

        # Create curve widget
        tk.Button(self.curve_frame, text='Create',
                command=self.create_curve, width=12).grid(
                row=2, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        # tk.Label(self.curve_frame, text='Curve: ID - name -> {0} - Curve'.format(Curve.count)).grid(row=2, column=1, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)  # TODO: StringVar() for label (needs update after curve creation)

        self.tool_notebook.add(self.curve_tab, text='Curve')


    def choose_dir(self):
        """Get the working directory path with file dialog

            Process the string of working directory to have no more than
            'MAX_STR_CREATE_CURVE' characters. So for any string longer than 'MAX_STR_CREATE_CURVE', the width of label widget is the same.
            This gives no change in layout.
        """
        self.work_dir = filedialog.askdirectory(title='Choose a working directory for CSV files')
        print('Direcory selected: ', self.work_dir)  # Only for debug.
        # MAX_STR_CREATE_CURVE-3 to take into account the '...' prefix to the final string.
        if len(self.work_dir) > (self.MAX_STR_CREATE_CURVE-3):
            temp = '...' + self.work_dir[-self.MAX_STR_CREATE_CURVE:]
            self.work_dir_txt.set(temp)
        else:
            self.work_dir_txt.set(self.work_dir)


    def create_curve(self):
        pass

    def choose_file(self):
        pass
