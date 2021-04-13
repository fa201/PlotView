# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    PlotView is summarized as PV in variable names.
"""

try:
    from collections import OrderedDict
    import sys
    import tkinter as tk
    from tkinter import font
    #from tkinter import messagebox as msg
    from tkinter import filedialog
    import tkinter.ttk as ttk
    import webbrowser
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    import pandas as pd
except ModuleNotFoundError as e:
        print('The necessary Python packages are not installed.\n' + str(e))
        print('Please check the required packages at https://github.com/fa201/PlotView.')


class Curve:
    """ Contains all the data relative to a curve.
        Class attribute 'count' is used to describe the curve ID 'id' and gives the number of curves cerated.
        'id' is the key of Cruve instances dictionary.
        This key will never change whereas the user-defined 'name' can change.

        The default plotting parameters are those below (user can change them).
        Attributes:
            - id : string -> ID of creation (0 prefixed if below 10)
            - name: string -> user-defined name. Can be changed in the PV session
            - file: string -> path to CSV file
            - data: dataframe -> contains (X,Y) points to be plotted
            - data_type: dictionary -> contains X header and Y header
            - visibility: boolean -> flag to show the curve in the plot or not
            - color: string -> color of the curve line
            - width: float -> width of the curve line
            - style: string -> style of the curve line
            - marker: string -> line marker (symbol) for the curve
            - marker_size: float -> size of line marker for the curve from 0.0 to 10.0
            TODO: add fig, ax, canvas, work_dir etc.
        Methods:
            - method to read the CSV file
    """
    count = 0
    # Dictionary of curve instances.
    dic = OrderedDict()

    def __init__(self, path):
        #self.id = str(Curve.count)
        self.name = 'Name'
        self.path = path
        self.data = self.read_file(path)
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
        # 'marker_size' = 0 -> not visible.
        self.marker_size = 0.0
        Curve.count += 1

    def read_file(self, path):
        """ Read the curve CSV file.

            It is necessary to convert data to float in 'read_csv' in order to plot.
            Requirements on the file format:
                - delete unused data and headers: header should be on the first line
                - rename column headers if necessary
                - only 2 columns of data
                - strip unwanted spaces
                - make sure that comma is the delimiter
                - decimal character is the point '.'
        """
        df = pd.read_csv(self.path, delimiter=',', dtype=float)
        return df


class Application(tk.Tk):
    """"It defines the main window of GUI."""
    def __init__(self):
        """ Initialize the main window.

            Constants:
            - PV_VERSION: string -> plot view version as shown by git tag.
            - WIN_RESIZABLE: boolean -> prevents the user from resizing the root window.
            - WIN_SIZE_POS: string -> window size (width x height) and position relative
                                      to top left corner.
            - FONT_SIZE: integer -> size of font to be used for all widget texts.
            - PLOT_WIDTH: float -> width (in) of matplotlib figure.
            - PLOT_HEIGHT: float -> height (in) of matplotlib figure.
            - MAX_STR_CREATE_CURVE: int -> number of caracters to be displayed to show the
                                           working directory.

            Variables:
            - work_dir: string -> directory path showing working directory.
            - work_dir_txt: string -> end of directory path showing working directory.
            - work_file: string -> file path to CSV file.
            - work_file_txt: string -> end of file path.
        """
        super().__init__()

        # ATTRIBUTES
        # Main window parameters.
        self.PV_VERSION = '0.4'
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
        # Max length of string showed by 'Create curve' labels.
        # This is related to window width, font, and font size.
        self.MAX_STR_CREATE_CURVE = 32

        # Working directory variables.
        # 'work_dir_set' defines the directory for the CSV filedialog.
        self.work_dir = ''
        self.work_dir_txt = tk.StringVar(self)
        self.work_dir_txt.set(self.create_underscores())
        # Path to CSV file
        # work_file define the CSV file path
        self.work_file = ''
        self.work_file_txt = tk.StringVar(self)
        self.work_file_txt.set(self.create_underscores())
        # Displayed working file path (only last characters.)
        # self.work_file_txt.set(self.work_file[-35:-1])
        # Curve creation label showing the curve name
        self.curve_label = tk.StringVar(self)
        self.curve_label.set('No CSV files selected.')

        # METHODS
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)
        self.window_setup()
        self.create_menus()
        self.create_plot_area()
        self.create_notebook()
        self.curve_tab()

    def create_underscores(self):
        """Creates a string with underscores to fill the 'work_dir' and 'work file' labels when empty."""
        underscores = list()
        for i in range(0, self.MAX_STR_CREATE_CURVE):
            underscores.append('_')
        return ''.join(underscores)

    def window_setup(self):
        """ Some basic setup is done on the GUI.

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
        my_font = tk.font.nametofont('TkDefaultFont')
        my_font.configure(size=self.FONT_SIZE)
        # Apply previous change to all widgets created since now.
        self.option_add("*Font", my_font)

        # STATUS BAR
        self.status_frame = tk.Frame(self)
        # The status frame should extend on all width of the main window.
        self.status_frame.pack(expand=False, fill=tk.X, side=tk.BOTTOM)
        # The status is initialized with empty message left aligned.
        self.status = tk.Label(self.status_frame, text=' Ready.', bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        # The label shoul expand on the total window width.
        self.status.pack(fill=tk.BOTH, expand=False)

    def app_quit(self):
        """ Quit the application."""
        # Destroy the main window.
        self.destroy()
        # Normal termination and free the stack.
        sys.exit(0)

    def create_menus(self):
        """ Create the menus and sub-menus of the main GUI.
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
        """ Plotview wiki is shown in web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/wiki/Help')
        self.set_status('The PlotView wiki page is shown in your web browser.')

    def licence_redirect(self):
        """ PlotView licence is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/blob/master/LICENSE')
        self.set_status('The page of GPL3 licence is shown in your web browser.')

    def about_redirect(self):
        """ PlotView repository is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')
        self.set_status('The PlotView repository on github was opened in your web browser.')

    def set_status(self, string):
        """ Update the status bar message.

        A space is added on the left to give more room relative to the window border.
        """
        self.status.config(text=' '+string)

    def create_plot_area(self):
        # Tip: https://stackoverflow.com/questions/29432683/resizing-a-matplotlib-plot-in-a-tkinter-toplevel
        self.fig = plt.Figure(figsize=(self.PLOT_WIDTH, self.PLOT_HEIGHT))
        self.ax = self.fig.add_subplot(111)
        self.mat_frame = tk.Frame(self)
        # mat_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.mat_frame.pack(expand=False, side=tk.LEFT)
        # Creates a drawing area to put the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mat_frame)
        self.canvas.draw()
        # Creates the Matplotlib navigation tool bar for figures.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.mat_frame)
        self.toolbar.draw()
        self.canvas.get_tk_widget().pack()

    def create_notebook(self):
        """ Notebook on RH panel containing all the tool tabs."""
        # Frame for RH panel. It contains the ttk.notebook.
        self.tool_frame = tk.Frame(self)
        self.tool_frame.pack(expand=True, fill=tk.BOTH)
        # Notebook
        self.tool_notebook = ttk.Notebook(self.tool_frame)
        self.tool_notebook.pack(expand=True, fill=tk.BOTH)

    def curve_tab(self):
        """ First tab managing curve creation."""
        # Create curve tab
        self.curve_tab = ttk.Frame(self.tool_notebook)

        # TODO: for 'create_curve_frame' and 'select_curve_frame' use columnspan ?
        # CREATE CURVE PANEL
        self.create_curve_frame = tk.LabelFrame(self.curve_tab, text='Create curve')
        self.create_curve_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                              padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY)
        # Working directory widgets
        tk.Button(self.create_curve_frame, text='Select directory',
                  command=self.choose_dir, width=12).grid(
                  row=0, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        tk.Label(self.create_curve_frame, textvariable=self.work_dir_txt).grid(
                 row=0, column=1, columnspan=3, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.W)
        # CSV file widgets
        tk.Button(self.create_curve_frame, text='Select CSV file',
                  command=self.choose_file, width=12).grid(
                  row=1, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        tk.Label(self.create_curve_frame, textvariable=self.work_file_txt).grid(
                 row=1, column=1, columnspan=3, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.W)
        # Create curve widgets
        self.curve_label = tk.StringVar()
        self.curve_label.set('Name')
        tk.Entry(self.create_curve_frame, textvariable=self.curve_label, width=30).grid(
                  row=2, column=0, columnspan=3, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        tk.Button(self.create_curve_frame, text='Create',
                  command=self.curve_create, width=6).grid(
                  row=2, column=3, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        
        # CURVE PROPERTIES
        self.curve_prop_frame = tk.LabelFrame(self.curve_tab, text='Curve properties')
        self.curve_prop_frame.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                              padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY)
        
        # Tip: https://stackoverflow.com/questions/54283975/python-tkinter-combobox-and-dictionary
        tk.Label(self.curve_prop_frame, text='Select ID of active curve').grid(row=0, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        self.active_curve_combo = ttk.Combobox(self.curve_prop_frame,
                                                values=list(Curve.dic.keys()),
                                                justify=tk.CENTER,
                                                width=4
                                                )
        self.active_curve_combo.grid(row=0, column=1, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        self.active_curve_combo.bind('<<ComboboxSelected>>', self.active_curve)

        self.show_state = tk.IntVar()
        self.show_state.set(1)
        show_check = tk.Checkbutton(self.curve_prop_frame,
                text='Show active curve',
                variable=self.show_state,
                indicatoron=0,
                command=self.show_check_update).grid(row=1, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)




        # Add this tab to the notebook.
        self.tool_notebook.add(self.curve_tab, text='Curve')

    def choose_dir(self):
        """ Get the working directory path with file dialog

            Process the string of working directory to have no more than 'MAX_STR_CREATE_CURVE'
            characters. So for any string longer than 'MAX_STR_CREATE_CURVE', the width of label
            widget is the same. This gives no change in layout when selecting long or short path.
            The length of string displayed should be the same as for 'choose_file'.
        """
        self.work_dir = filedialog.askdirectory(title='Choose a working directory for CSV files')
        # MAX_STR_CREATE_CURVE-3 to take into account the '...' prefix to the final string.
        if len(self.work_dir) > (self.MAX_STR_CREATE_CURVE-3):
            temp = '...' + self.work_dir[-self.MAX_STR_CREATE_CURVE+3:]
            self.work_dir_txt.set(temp)
            self.set_status('Working directory is set at:'+self.work_dir)
        elif 0 < len(self.work_dir) < (self.MAX_STR_CREATE_CURVE-3):
            self.work_dir_txt.set(self.work_dir)
            self.set_status('Working directory is set at:'+self.work_dir)
        else:
            # CANCEL return empty string. So I reaffect the initial value to keep the layout.
            self.work_dir_txt.set(self.create_underscores())
            self.set_status('WARNING - No working directory selected.')

    def choose_file(self):
        """ Get the path to the CSV file to open.

            Process the string of file path to have no more than 'MAX_STR_CREATE_CURVE' characters.
            So for any string longer than 'MAX_STR_CREATE_CURVE', the width of label widget is
            the same. This gives no change in layout when selecting long or short path.
            The length of string displayed should be the same as for 'choose_dir'.
        """
        self.work_file = filedialog.askopenfilename(
            initialdir=self.work_dir, filetypes=[('CSV file', '*.csv')], title='Open CSV file')
        # print('Path of file selected:', self.work_file)  # Only for debug.
        # MAX_STR_CREATE_CURVE-3 to take into account the '...' prefix to the final string.
        if len(self.work_file) > (self.MAX_STR_CREATE_CURVE-3):
            temp = '...' + self.work_file[-self.MAX_STR_CREATE_CURVE+3:]
            self.work_file_txt.set(temp)
            self.set_status('CSV file selected: '+self.work_file)
        elif 0 < len(self.work_file) < (self.MAX_STR_CREATE_CURVE-3):
            self.work_file_txt.set(self.work_file)
            self.set_status('CSV file selected: '+self.work_file)
        else:
            # CANCEL return empty string. So I reaffect the initial value to keep the layout.
            self.work_file_txt.set(self.create_underscores())
            self.set_status('WARNING - A CSV file has to be selected.')

    def curve_create(self):
        """Create the Curve instance from the CSV file given by 'work_file'

        The curve is added in the Curve.curves list. Index is Curve.count.
        """
        if self.work_file:
            # Since instance is not yet created self.id does not exist. So 'count' is used.
            Curve.dic[str(Curve.count)] = (Curve(self.work_file))
            # Show the name of the created curve in 'curve_label'
            #self.curve_label.set(Curve.dic[str(Curve.count)].name)
            Curve.dic[str(Curve.count)].name = self.curve_label.get()
            self.update_active_curve_combo()
            self.plot_curves()
        else:
            self.set_status('ERROR - No CSV file were selected.')

    def plot_curves(self):
        """Plot all curves with visibility = True"""
        # It is necessary to clear the Axes since the for loop starts from 1
        # for every curve plot. Otherwise curve_01 get duplicated for each call.
        self.ax.clear()
        for i in range(1, Curve.count+1):
            if Curve.dic[str(i)].visibility:
                self.ax.plot(Curve.dic[str(i)].data.iloc[:, 0],
                             Curve.dic[str(i)].data.iloc[:, 1],
                             label=Curve.dic[str(i)].name,
                             color=Curve.dic[str(i)].color,
                             lw=Curve.dic[str(i)].width,
                             ls=Curve.dic[str(i)].style,
                             marker=Curve.dic[str(i)].marker,
                             markersize=Curve.dic[str(i)].marker_size
                             )
                self.set_status(Curve.dic[str(i)].name+' is plotted.')
        self.ax.legend(loc='lower right')
        self.canvas.draw()
        self.set_status('Plot is updated.')

    def update_active_curve_combo(self):
        l = list(Curve.dic.keys())
        self.active_curve_combo['values'] = tuple(l)

    def active_curve(self, event):
        try:
            self.selected_curve = event.widget.get()
            print('Selected curve :', self.selected_curve)
        except AttributeError:
            self.set_status('WARNING - There is no curve defined.')
        # TODO: get all the curve attribute form the selected curve to update widgets.
        # TODO: status of curve selected

    def show_check_update(self):
        """ Process the 'show' check toggle."""
        print('Show state: ', self.show_state.get())
        try:
            print('Selected curve in show_check_update:', self.selected_curve)
            Curve.dic[self.selected_curve].visibility = self.show_state.get()
            # 'plot_curves' should be in try so that it is not launched in case of Exception.
            # This allows to have the warning message persistent.
            self.plot_curves()
        except AttributeError:
            self.set_status('WARNING - There is no curve defined.')
        # TODO: launch plot_curves after clicking on 'Apply' button.
        # TODO: link Curve.dic[self.selected_curve].visibility avec set() en premier ?
        

if __name__ == '__main__':
    app = Application()
    # Launch the GUI mainloop which should always be the last instruction!
    app.mainloop()
