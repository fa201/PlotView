# -*- coding: utf-8 -*-

""" PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    Licence: GN GPL-3.0
    PlotView is summarized as PV in variable names.
"""


try:
    from collections import OrderedDict
    import configparser
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    from matplotlib.ticker import MaxNLocator
    import os
    import pandas as pd
    import sys
    import tkinter as tk
    from tkinter import font
    from tkinter import messagebox as msg
    from tkinter import filedialog
    import tkinter.ttk as ttk
    import webbrowser
except ModuleNotFoundError as e:
        print('The necessary Python packages are not installed.\n' + str(e))
        print('Please check the required packages at https://github.com/fa201/PlotView.')


# Constants for curve styling properties.
# Set of color for a white background. Change the set for a black background.
my_colors = {'white_bg': ['white', 'black', 'grey', 'red', 'darksalmon', 
						  'sienna', 'tan', 'gold', 'green', 'dodgerblue', 
						  'blueviolet', 'hotpink', 'orange', 'peru', 
						  'limegreen', 'turquoise', 'royalblue'
			             ],
			 'black_bg': ['black', 'white', 'grey', 'red', 'darksalmon', 
			  			  'sienna', 'tan', 'gold', 'green', 'dodgerblue', 
			  			  'blueviolet', 'hotpink', 'orange', 'peru', 
			  			  'limegreen', 'turquoise', 'royalblue'
			             ]
			}
my_linestyles = ['solid', 'dashed', 'dotted']


class Curve:
    """ Contains all the data relative to a curve.
        Class attribute 'count' is used the curve ID 'id' and gives the number of curves created.
        'id' is the key of Cruve instances dictionary.
        This key will never change whereas the user-defined 'name' can change.

        The default plotting parameters are those below (user can change them).
        Attributes:
            - name: string -> user-defined name. Can be changed in the PV session
            - path: string -> path to CSV file
            - data_in: dataframe -> contains (X,Y) points as read in the CSV file
            - data_type: dictionary -> contains X header and Y header
            - data_out: dataframe -> data_in with offset and scale values to be plotted
            - visibility: boolean -> flag to show the curve in the plot or not
            - color: string -> color of the curve line
            - width: float -> width of the curve line
            - style: string -> style of the curve line
            - x_offset: float -> X data offset after X data scale
            - y_offset: float -> Y data offset after Y data scale
            - x_scale: float -> X data scaling
            - y_scale: float -> Y data scaling
            TODO: add fig, ax, canvas, work_dir etc.
        Methods:
            - method to read the CSV file
    """
    count = 0
    # Dictionary of curve instances.
    dic = OrderedDict()

    def __init__(self, path):
        """ Create a Curve instance based on CSV file path.

            TODO: add all attributes in parameter to create a Curve when reading session file
        """
        self.name = 'Name'
        self.path = path
        self.data_in = self.read_file(self.path)
        self.data_type = self.get_data_types()
        self.data_out = self.create_data_out(self.data_in)
        self.visibility = True
        self.color = my_colors[app.plot_fig_color][1]
        self.width = 1.0
        self.style = my_linestyles[0]
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.x_scale = 1.0
        self.y_scale = 1.0
        self.ext_x_min = 0.0
        self.ext_x_min_y = 0.0
        self.ext_x_max = 0.0
        self.ext_x_max_y = 0.0
        self.ext_y_min = 0.0
        self.ext_y_min_x = 0.0
        self.ext_y_max = 0.0
        self.ext_y_max_x = 0.0
        Curve.count += 1

    def read_file(self, path):
        """ Read the curve CSV file.

            It is necessary to convert data to float in 'read_csv' in order to plot.
            Requirements on the file format:
                - delete unused data and headers: header should be on the first line
                - rename column headers if necessary
                - only 2 columns of data (there is no error for 1 column of data but no curve is visible)
                - make sure that comma is the delimiter
                - decimal character is the point '.'
        """
        try:
            df = pd.read_csv(self.path, delimiter=',', dtype=float)
            print('CSV file read:', self.path)
            print(df)
            return df
        except (TypeError, ValueError, IndexError, AttributeError) as e:
            msg.showerror('Error', 'The format of CSV file is not correct.\nPlease refer to files in the "test" folder.')
            Application.choose_file(app)
        # TODO: handle following exceptions: no column, more than 2 columns, strings, missing values, etc.

    def get_data_types(self):
        temp = {}
        temp['x_type'] = self.data_in.columns[0]
        temp['y_type'] = self.data_in.columns[1]
        return temp

    def create_data_out(self, df):
        temp = df.copy()
        return temp

    def find_extrema(self):
        """ all values are round to 10 -> use a variable and update first label in extrema plot (number of digits)

            since pd.round() gives error on Windows, rounding is done on the float.
            The extrema values displayed on GUI are rounded but printed values are not.
        """
        print('Extrema values for curve', self.name, 'without rounding:')
        
        # X min
        temp_ext_x_min = self.data_out.iloc[:, 0].min()
        self.ext_x_min = round(temp_ext_x_min, app.ROUND)
        # Find Y for X min
        temp_ext_x_min_y = self.data_out.iloc[self.data_out.iloc[:, 0].idxmin(), 1]
        self.ext_x_min_y = round(temp_ext_x_min_y, app.ROUND)
        print('X min:', temp_ext_x_min, ' @ Y:', temp_ext_x_min_y)
        app.extrema_x_min.set('X min ' + str(self.ext_x_min) + ' @ Y ' + str(self.ext_x_min_y))
        
        # X max
        temp_ext_x_max = self.data_out.iloc[:, 0].max()
        self.ext_x_max = round(temp_ext_x_max, app.ROUND)
        # Find Y for X max
        temp_ext_x_max_y = self.data_out.iloc[self.data_out.iloc[:, 0].idxmax(), 1]
        self.ext_x_max_y = round(temp_ext_x_max_y, app.ROUND)
        print('X max:', temp_ext_x_max, ' @ Y:', temp_ext_x_max_y)
        app.extrema_x_max.set('X max ' + str(self.ext_x_max) + ' @ Y ' + str(self.ext_x_max_y))

        # Y min
        temp_ext_y_min = self.data_out.iloc[:, 1].min()
        self.ext_y_min = round(temp_ext_y_min, app.ROUND)
        # Find X for Y min
        temp_ext_y_min_x = self.data_out.iloc[self.data_out.iloc[:, 1].idxmin(), 0]
        self.ext_y_min_x = round(temp_ext_y_min_x, app.ROUND)
        print('Y min:', temp_ext_y_min, '@ X:', temp_ext_y_min_x)
        app.extrema_y_min.set('Y min ' + str(self.ext_y_min) + ' @ X ' + str(self.ext_y_min_x))

        # Y max
        temp_ext_y_max = self.data_out.iloc[:, 1].max()
        self.ext_y_max = round(temp_ext_y_max, app.ROUND)
        # Find X for Y max
        temp_ext_y_max_x = self.data_out.iloc[self.data_out.iloc[:, 1].idxmax(), 0]
        self.ext_y_max_x = round(temp_ext_y_max_x, app.ROUND)
        print('Y max:', temp_ext_y_max, '@ X:', temp_ext_y_max_x)
        app.extrema_y_max.set('Y max ' + str(self.ext_y_max) + ' @ X ' + str(self.ext_y_max_x))


class Application(tk.Tk):
    """"It defines the main window of GUI."""
    def __init__(self):
        """ Initialize the main window.

            The window is launched with a size of 1280 x 720 but it can be resized.
            The matplotlib are is defined 16 x 12 in which is bigger than the available space.
            Yet it is not a problem because it is handled by tk window manager.

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

            Methods: they launch the window layout setup, and create the tab on the RH side for tools.
        """
        super().__init__()

        # ATTRIBUTES
        # Main window parameters.
        self.PV_VERSION = '1.8'
        self.WIN_SIZE_POS = '1280x780'
        self.FONT_SIZE = 9
        # Matplotlib parameters.
        self.PLOT_WIDTH = 16
        self.PLOT_HEIGHT = 12
        # Parameters for widgets on RH tool panel.
        # Padding for all containers to uniformize the look
        self.CONTAINER_PADX = 10
        self.CONTAINER_PADY = 6.5 
        # Padding for all widgets inside a container
        self.WIDGET_PADX = 2.5
        self.WIDGET_PADY = 2.5
        # Max length of string showed by 'Create curve' labels.
        # This is related to window width, font, and font size.
        self.MAX_STR_CREATE_CURVE = 39

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
        # Curve creation label showing the curve name
        self.curve_label = tk.StringVar(self)
        self.curve_label.set('No CSV files selected.')

        # Number of decimals for rounding operation
        self.ROUND = 5

        # TTK styling. Does not work for TEntry, TCombobox
        s = ttk.Style()
        # Options: default, clam, alt, classic
        s.theme_use('alt')
        # Buttons
        s.configure('w4.TButton', width=4)
        s.configure('w4.TButton', width=6)
        s.configure('w4.TButton', width=9)

        # METHODS
        # Allows root window to be closed by the closing icon.
        self.protocol('WM_DELETE_WINDOW', self.app_quit)
        # Setup the loayout of the main window.
        self.window_setup()
        # Create the tool 'Curve' tab on the RH side
        self.curve_tab()
        # Create the tool 'Plot' tab on the RH side
        self.plot_tab()
        # Create the tool 'Annotation' tab on the RH side
        self.annotation_tab()
        # Create the tool 'Extrema' tab on the RH side
        self.extrema_tab()

    def create_underscores(self):
        """ Creates a string with underscores to fill the 'work_dir' and 'work file' labels when empty.
            Empty label and filled label are both limited to 'MAX_STR_CREATE_CURVE' characters.
            This way, the label layout is visually more consistent.
        """
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
            The matplotlib area is draw on the left side.
            The tool widgets on the right side will be in a notebook to have tabs to save room on layout.
            The menu is created at top with disabled buttons when functions are not implemented.
        """
        # WINDOW
        self.title('PlotView ' + self.PV_VERSION)
        self.geometry(self.WIN_SIZE_POS)

        # FONT
        # https://stackoverflow.com/questions/31918073/tkinter-how-to-set-font-for-text
        my_font = tk.font.nametofont('TkDefaultFont')
        my_font.configure(size=self.FONT_SIZE)
        # Apply previous change to all widgets created since now.
        self.option_add("*Font", my_font)

        # MENUS
        menu_main = tk.Menu(self)
        # Menu tear off is disabled.
        menu_file = tk.Menu(menu_main, tearoff='False')
        menu_pref = tk.Menu(menu_main, tearoff='False')
        menu_help = tk.Menu(menu_main, tearoff='False')
        # Add menu_file in menu_main
        menu_main.add_cascade(label='File', menu=menu_file)
        menu_main.add_cascade(label='Help', menu=menu_help)
        # Link of main menu to root window
        self.config(menu=menu_main)
        # File Menu
        menu_file.add_command(label='Load session', command=self.load_session)
        menu_file.add_command(label='Save session', command=self.save_session)
        menu_file.add_separator()
        menu_file.add_command(label='Quit', command=self.app_quit)
        # Help Menu
        menu_help.add_command(label='Help files', command=self.help_message)
        menu_help.add_command(label='Licence', command=self.licence_message)
        menu_help.add_separator()
        menu_help.add_command(label='About', command=self.about_redirect)

        # CREATE STATUS BAR AT BOTTOM
        self.status_frame = ttk.Frame(self)
        # Create the sizegrip align on lower edge with status bar.
        self.sg = ttk.Sizegrip(self.status_frame)
        self.sg.pack(side=tk.RIGHT)
        # The status frame should extend on all width of the main window.
        self.status_frame.pack(expand=False, fill=tk.X, side=tk.BOTTOM)
        # The status is initialized with empty message left aligned.
        self.status = ttk.Label(self.status_frame,
                               text=' Ready.',
                               relief=tk.SUNKEN,
                               anchor=tk.W,
                               )
        # The label shoul expand on the total window width.
        self.status.pack(fill=tk.BOTH, expand=False)

        # CREATE A NOTEBOOK ON THE RIGHT FOR TOOL WIDGETS
        # Frame for RH panel. It contains the ttk.notebook.
        # This panel needs to be defined before the matplotlib frame.
        self.tool_frame = ttk.Frame(self)
        self.tool_frame.pack(expand=False, fill=tk.BOTH, side=tk.RIGHT)
        # Notebook with padding only on the left
        self.tool_notebook = ttk.Notebook(self.tool_frame)
        self.tool_notebook.pack(expand=True, fill=tk.BOTH)

        # CREATE PLOT AREA ON THE LEFT
        # Tip: https://stackoverflow.com/questions/29432683/resizing-a-matplotlib-plot-in-a-tkinter-toplevel
        self.fig = plt.Figure(figsize=(self.PLOT_WIDTH, self.PLOT_HEIGHT))
        self.ax = self.fig.add_subplot(111)
        # Color setting according to plot backgroung color
        # plot_fig_color is initialized here but the value will be updatedbased on radiobutton state
        self.plot_fig_color = 'white_bg'
        self.mat_frame = ttk.Frame(self)
        self.mat_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        # Creates a drawing area to put the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mat_frame)
        self.canvas.draw()
        # Creates the Matplotlib navigation tool bar for figures.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.mat_frame)
        #self.toolbar.draw() shows a bug with matplotlib 3.5
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def app_quit(self):
        """ Quit the application and free the stack."""
        self.destroy()
        sys.exit(0)

    def help_message(self):
        """ Give directions to help files."""
        m1 = 'Help is available in the "test" folder with the "index.html" file. '
        m2 = 'In case you have not downloaded this folder, it is available at:\n'
        m3 = 'https://github.com/fa201/PlotView'
        msg.showinfo('Help', m1+m2+m3)

    def licence_message(self):
        """ Give directions to the licence file."""
        m1 = 'PlotView is licensed under GNU GPL-3.0. '
        m2 = 'In case you have not downloaded the "LICENSE" file, it is available at:\n'
        m3 = 'https://github.com/fa201/PlotView'
        msg.showinfo('License', m1+m2+m3)

    def about_redirect(self):
        """ PlotView repository is shown in the web browser."""
        webbrowser.open_new_tab('https://github.com/fa201/PlotView/')
        self.set_status('The PlotView repository on github was opened in your web browser.')

    def set_status(self, string):
        """ Update the status bar message.

            A space is added on the left to give more room relative to the window border.
        """
        self.status.config(text=' '+string)

    def save_session(self):
        """ Save session as a config file

            Curve data are exported.
            Plot data are exported.
            The session file will be created each time so the previous one is erased.
        """
        session_file = filedialog.asksaveasfilename(
            initialdir=self.work_dir, filetypes=[('PV session file', '*.pv')], title='Save as PlotView session file')
        # Case if CANCEL is clicked after selecting a session file. Then session_file=''. 
        if session_file == '':
            self.set_status('No session file selected.')   
        # Case if CANCEL is clicked without selecting a session file. Then session_file=(), empty tuple. 
        elif isinstance(session_file, tuple):
            self.set_status('No session file selected.')    
        else:
            config = configparser.ConfigParser()
            # Plot data
            config['plot'] = {'main title': self.main_title.get(),
                              'x title': self.x_title.get(),
                              'y title': self.y_title.get(),
                              'auto scale': self.autoscale.get(),
                              'x min user range': self.x_min_range.get(),
                              'x max user range': self.x_max_range.get(),
                              'y min user range': self.y_min_range.get(),
                              'y max user range': self.y_max_range.get(),
                              'x number of ticks': self.x_bin.get(),
                              'y number of ticks': self.y_bin.get(),
                              'legend position': self.legend.get(),
                              'display grid': self.grid_state.get(),
                              'background color': self.fig_color_flag.get()
                              }
            # Annotation and arrow data
            config['annotation'] = {'text': self.annotation.get(),
                                    'text X pos.': self.annotation_x.get(),
                                    'text Y pos.': self.annotation_y.get(),
                                    'text color': self.annot_color_combo.get(),
                                    'text size': self.annot_size.get(),
                                    'text state': self.annot_state.get(),
                                    'arrow head X pos.': self.arrow_head_x.get(),
                                    'arrow head Y pos.': self.arrow_head_y.get(),
                                    'arrow head length': self.arrow_head_length.get(),
                                    'arrow head width': self.arrow_head_width.get(),
                                    'arrow color': self.arrow_color_combo.get(),
                                    'arrow line width': self.arrow_width.get(),
                                    'arrow state': self.arrow_state.get(),
                                   }
            # Session info
            config['session'] = {'working directory': self.work_dir,
                                 'curve count': Curve.count,
                                }
            # Curve data
            for i in range(1, Curve.count+1):
                config[i] = {'name': Curve.dic[str(i)].name,
                             'CSV file path': Curve.dic[str(i)].path,
                             'X data': Curve.dic[str(i)].data_type['x_type'],
                             'Y data': Curve.dic[str(i)].data_type['y_type'],
                             'visibility': Curve.dic[str(i)].visibility,
                             'line color': Curve.dic[str(i)].color,
                             'line width': Curve.dic[str(i)].width,
                             'line style': Curve.dic[str(i)].style,
                             'offset in X': Curve.dic[str(i)].x_offset,
                             'offset in Y': Curve.dic[str(i)].y_offset,
                             'scale in X': Curve.dic[str(i)].x_scale,
                             'scale in Y': Curve.dic[str(i)].y_scale
                            }
            # Write the file and erase existing file.
            with open(session_file, 'w') as file:
                config.write(file)
            self.set_status('Session file is saved at: ' + session_file)

    def load_session(self):
        """ Load session file 

            Curve data are read.
            Plot data are read.
        """
        config = configparser.ConfigParser()
        # TODO: Show a warning or ask a permission since the work will be lost ?
        # Read the sessionfile
        session_file = filedialog.askopenfilename(
            initialdir=self.work_dir, filetypes=[('PV session file', '*.pv')], title='Open PlotView session file')
        # Case if CANCEL is clicked without selecting a session file. Then session_file=(), empty tuple.
        if isinstance(session_file, tuple):
            self.set_status('No session file selected.')    
        # Make sure the path to session file exists.
        elif os.path.exists(session_file):
            config.read(session_file)
            # Process Plot section
            self.main_title.set(config.get('plot', 'main title'))
            self.x_title.set(config.get('plot', 'x title'))
            self.y_title.set(config.get('plot', 'y title'))
            self.autoscale.set(config.getboolean('plot', 'auto scale'))
            self.x_min_range.set(config.get('plot', 'x min user range'))
            self.x_max_range.set(config.get('plot', 'x max user range'))
            self.y_min_range.set(config.get('plot', 'y min user range'))
            self.y_max_range.set(config.get('plot', 'y max user range'))
            self.x_bin.set(config.get('plot', 'x number of ticks'))
            self.y_bin.set(config.get('plot', 'y number of ticks'))
            self.legend.set(config.getint('plot', 'legend position'))
            self.grid_state.set(config.getboolean('plot', 'display grid'))
            self.fig_color_flag.set(config.get('plot', 'background color'))
            # Process Annotation section
            self.annotation.set(config.get('annotation', 'text'))
            self.annotation_x.set(config.getfloat('annotation', 'text X pos.'))
            self.annotation_y.set(config.getfloat('annotation', 'text Y pos.'))
            self.annot_color_combo.set(config.get('annotation', 'text color'))
            self.annot_size.set(config.get('annotation', 'text size'))
            self.annot_state.set(config.getboolean('annotation', 'text state'))
            self.arrow_head_x.set(config.getfloat('annotation', 'arrow head X pos.'))
            self.arrow_head_y.set(config.getfloat('annotation', 'arrow head Y pos.'))
            self.arrow_head_length.set(config.get('annotation', 'arrow head length'))
            self.arrow_head_width.set(config.get('annotation', 'arrow head width'))
            self.arrow_color_combo.set(config.get('annotation', 'arrow color'))
            self.arrow_width.set(config.get('annotation', 'arrow line width'))
            self.arrow_state.set(config.getboolean('annotation', 'arrow state'))
            # Process session data
            self.work_dir = config.get('session', 'working directory')
            # Display the working directory
            if len(self.work_dir) > (self.MAX_STR_CREATE_CURVE-3):
                temp = '...' + self.work_dir[-self.MAX_STR_CREATE_CURVE+3:]
                self.work_dir_txt.set(temp)
                self.set_status('Working directory is set at:'+self.work_dir)
            elif 0 < len(self.work_dir) < (self.MAX_STR_CREATE_CURVE-3):
                self.work_dir_txt.set(self.work_dir)
                self.set_status('Working directory is set at:'+self.work_dir)
            Curve.count = config.getint('session', 'curve count')
            # Process Curve data
            for i in range(1, Curve.count+1):
                if config.get(str(i), 'csv file path'):
                    Curve.dic[str(i)] = Curve(config.get(str(i), 'csv file path'))
                    # Since Curve.count is incremented after curve creation, it needs to be decremented.
                    Curve.count -= 1
                    Curve.dic[str(i)].name = config.get(str(i), 'name')
                    Curve.dic[str(i)].data_type['x_type'] = config.get(str(i), 'x data')
                    Curve.dic[str(i)].data_type['y_type'] = config.get(str(i), 'y data')
                    Curve.dic[str(i)].visibility = config.get(str(i), 'visibility')
                    Curve.dic[str(i)].color = config.get(str(i), 'line color')
                    Curve.dic[str(i)].width = config.get(str(i), 'line width')
                    Curve.dic[str(i)].style = config.get(str(i), 'line style')
                    Curve.dic[str(i)].x_offset = config.getfloat(str(i), 'offset in X')
                    Curve.dic[str(i)].y_offset = config.getfloat(str(i), 'offset in Y')
                    Curve.dic[str(i)].x_scale = config.getfloat(str(i), 'scale in X')
                    Curve.dic[str(i)].y_scale = config.getfloat(str(i), 'scale in Y')
                else:
                    msg.showerror('Error', 'No CSV file were selected for curve'+str(i))
            # Update curve ID list to be able to continue working on curves.
            self.active_curve_combo['values'] = tuple(list(Curve.dic.keys()))
            # Update curve list for Extrema
            self.active_curve_combo2['values'] = tuple(list(Curve.dic.keys()))
            # Update background color for plot
            self.update_plot_bg_color()
            self.set_status('Data in session file "PV_session.ini" are read.')
            self.plot_curves()
        else:
            # Case if CANCEL is clicked after selecting a session file.
            self.set_status('No session file selected.')       

    def curve_tab(self):
        """ First tab managing curve creation.

            Label variables are local variables so no 'self' prepend.
        """
        # Create curve tab
        self.curve_tab = ttk.Frame(self.tool_notebook)
        # Allow the column to expand for children
        self.curve_tab.columnconfigure(index=0, weight=1)

        # CREATE CURVE PANEL
        self.create_curve_frame = ttk.LabelFrame(self.curve_tab, text='Create curve')
        self.create_curve_frame.grid(row=0, column=0)
        # Allow the column to expand for children
        for i in range(0, 2):
            self.create_curve_frame.columnconfigure(index=i, weight=1)

        # Working directory widgets
        ttk.Button(self.create_curve_frame, text='Work dir.',
                  command=self.choose_dir, style='w9.TButton'
                  ).grid(row=0, column=0)
        ttk.Label(self.create_curve_frame,
                 textvariable=self.work_dir_txt
                 ).grid(row=0, column=1)
        
        # CSV file widget
        ttk.Button(self.create_curve_frame, text='CSV file',
                  command=self.choose_file, style='w9.TButton'
                 ).grid(row=1, column=0)
        ttk.Label(self.create_curve_frame, textvariable=self.work_file_txt
                ).grid(row=1, column=1)
        # Curve name widget
        curve_name_label = ttk.Label(self.create_curve_frame, text='Curve name'
                )
        curve_name_label.grid(row=2, column=0)
        self.curve_label = tk.StringVar()
        self.curve_label.set('Curve_name')
        ttk.Entry(self.create_curve_frame, textvariable=self.curve_label, width=30,
                 justify=tk.CENTER).grid(row=2, column=1)
        # Curve create widget
        ttk.Button(self.create_curve_frame, text='Create curve',
                  command=self.curve_create, style='w4.TButton'
                 ).grid(row=3, column=0, columnspan=2)

        # CURVE PROPERTIES
        self.curve_prop_frame = ttk.LabelFrame(self.curve_tab, text='Curve properties')
        self.curve_prop_frame.grid(row=2, column=0)
        # Allow the column to expand for children
        for i in range(0, 5):
            self.curve_prop_frame.columnconfigure(index=i, weight=1)
    
        # Active curve selection
        # Tip: https://stackoverflow.com/questions/54283975/python-tkinter-combobox-and-dictionary
        select_curve_label = ttk.Label(self.curve_prop_frame, text='Select curve')
        select_curve_label.grid(row=0, column=0)
        self.active_curve_combo = ttk.Combobox(self.curve_prop_frame,
                                               values=list(Curve.dic.keys()),
                                               justify=tk.CENTER,
                                               width=4,
                                               )
        self.active_curve_combo.grid(row=0, column=1)
        # Set self.selected_curve here to avoid error if update_curve() is called without any curve selected.
        self.selected_curve = None
        self.active_curve_combo.bind('<<ComboboxSelected>>', self.active_curve)

        # Show curve
        self.show_state = tk.IntVar()
        self.show_state.set(1)
        ttk.Checkbutton(self.curve_prop_frame, text='Show curve',
                       variable=self.show_state
                      ).grid(row=0, column=2, columnspan=2)
        # Curve Name
        self.active_curve_name = tk.StringVar()
        self.active_curve_name.set(' ')
        name_label = ttk.Label(self.curve_prop_frame, text='Curve name'
                )
        name_label.grid(row=1, column=0)
        ttk.Entry(self.curve_prop_frame, textvariable=self.active_curve_name,
                 width=30, justify=tk.CENTER
                ).grid(row=1, column=1, columnspan=3)
        # Curve X data type.
        self.active_curve_x_data = tk.StringVar()
        self.active_curve_x_data.set(' ')
        ttk.Label(self.curve_prop_frame, text='Title for X data').grid(row=2, column=0)
        self.x_data_label = ttk.Label(self.curve_prop_frame, textvariable=self.active_curve_x_data,
                 width=30, justify=tk.CENTER)
        self.x_data_label.configure(anchor='center')
        self.x_data_label.grid(row=2, column=1, columnspan=3)
        # Curve Y data type.
        self.active_curve_y_data = tk.StringVar()
        self.active_curve_y_data.set(' ')
        ttk.Label(self.curve_prop_frame, text='Title for Y data').grid(row=3, column=0)
        self.y_data_label = ttk.Label(self.curve_prop_frame, textvariable=self.active_curve_y_data,
                 width=30, justify=tk.CENTER)
        self.y_data_label.configure(anchor='center')
        self.y_data_label.grid(row=3, column=1, columnspan=3)
        # Curve color
        line_color_label = ttk.Label(self.curve_prop_frame, text='Line color'
                )
        line_color_label.grid(row=4, column=0)
        self.curve_color_combo = ttk.Combobox(self.curve_prop_frame,
                                                values=my_colors[self.plot_fig_color],
                                                justify=tk.CENTER,
                                                width=12
                                                )
        self.curve_color_combo.set(my_colors[self.plot_fig_color][1])
        self.curve_color_combo.grid(row=4, column=1, columnspan=2)
        self.curve_color_combo.bind('<<ComboboxSelected>>', self.change_curve_color)
        # Line width
        line_width_label = ttk.Label(self.curve_prop_frame, text='Line width'
                )
        line_width_label.grid(row=5, column=0)
        self.curve_width = tk.StringVar()
        self.curve_width.set('1')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_width, width=4, justify=tk.CENTER).grid(
                  row=5, column=1)
        # Line style
        line_style_label = ttk.Label(self.curve_prop_frame,
                text='Line style')
        line_style_label.grid(row=5, column=2)
        self.curve_style_combo = ttk.Combobox(self.curve_prop_frame,
                                                values=my_linestyles,
                                                justify=tk.CENTER,
                                                width=3
                                                )
        self.curve_style_combo.set(my_linestyles[0])
        self.curve_style_combo.grid(row=5, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                    padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                   )
        self.curve_style_combo.bind('<<ComboboxSelected>>', self.change_curve_style)
        # X scale
        x_scale_label = ttk.Label(self.curve_prop_frame, text='Scale X axis'
                )
        x_scale_label.grid(row=6, column=0)
        self.curve_x_scale = tk.StringVar()
        self.curve_x_scale.set('1')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_x_scale, width=8,
                 justify=tk.CENTER).grid(row=6, column=1)
        # Y scale
        y_scale_label = ttk.Label(self.curve_prop_frame, text='Scale Y axis'
                )
        y_scale_label.grid(row=6, column=2)
        self.curve_y_scale = tk.StringVar()
        self.curve_y_scale.set('1')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_y_scale, width=8,
                 justify=tk.CENTER).grid(row=6, column=3)
        # X offset
        x_offset_label = ttk.Label(self.curve_prop_frame, text='Offset X axis'
                )
        x_offset_label.grid(row=7, column=0)
        self.curve_x_offset = tk.StringVar()
        self.curve_x_offset.set('0')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_x_offset, width=8,
                 justify=tk.CENTER).grid(row=7, column=1)
        # Y offset
        y_offset_label = ttk.Label(self.curve_prop_frame, text='Offset Y axis'
                )
        y_offset_label.grid(row=7, column=2)
        self.curve_y_offset = tk.StringVar()
        self.curve_y_offset.set('0')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_y_offset, width=8,
                 justify=tk.CENTER).grid(row=7, column=3)

        # APPLY BUTTON
        ttk.Button(self.curve_prop_frame, text='Apply curve properties',
                  command=self.update_curve, style='w6.TButton'
                 ).grid(row=8, column=0, columnspan=4)

        # APPLY PADDING AND STICKINESS ON WIDGETS CHILDREN AFTER THEY ARE CREATED
        # For self.curve_tab frame
        for frame in self.curve_tab.winfo_children():
            frame.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S,
                                 padx=self.CONTAINER_PADX, 
                                 pady=self.CONTAINER_PADY
                                )
        # For self.create_curve_frame self.curve_prop_frame frames
        union_list = (set(self.create_curve_frame.winfo_children()) |
                      set(self.curve_prop_frame.winfo_children())
                     )
        for widget in union_list:
            widget.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S, 
                                  padx=self.WIDGET_PADX, 
                                  pady=self.WIDGET_PADY
                                 )
        
        # Add this tab to the notebook.
        self.tool_notebook.add(self.curve_tab, text='Curve')

    def choose_dir(self):
        """ Get the working directory path with file dialog

            Process the string of working directory to have no more than 'MAX_STR_CREATE_CURVE'
            characters. This gives no change in layout when selecting long or short path.
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

            Process the string of working directory to have no more than 'MAX_STR_CREATE_CURVE'
            characters. This gives no change in layout when selecting long or short path.
            The length of string displayed should be the same as for 'choose_dir'.
        """
        self.work_file = filedialog.askopenfilename(
            initialdir=self.work_dir, filetypes=[('CSV file', '*.csv')], title='Open CSV file')
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
        """ Create the Curve instance from the CSV file given by 'work_file'

            First, check that the selected file exists. If not show an error message.
            Second, check that curve label is not empty. If not show an error message.
            The curve is added in the Curve.dic. Index is Curve.count.
        """
        if self.work_file:
            if len(self.curve_label.get()) != 0:
                # Since instance is not yet created self.id does not exist. So 'count' is used.
                Curve.dic[str(Curve.count)] = (Curve(self.work_file))
                # FIXME: si le CSV est mauvais il faut sortir de cette fonction.
                # Show the name of the created curve in 'curve_label'
                Curve.dic[str(Curve.count)].name = self.curve_label.get()
                # Update the list of curve for future modifications.
                self.active_curve_combo['values'] = tuple(list(Curve.dic.keys()))
                self.active_curve_combo2['values'] = tuple(list(Curve.dic.keys()))
                self.plot_curves()
            else:
                msg.showerror('Error', 'The name of the curve is required.')
        else:
            msg.showerror('Error', 'No CSV file were selected.')

    def update_curve(self):
        """ Update Curve instance attributes based on GUI input"""
        # Update curve name after testing is a curve was selected
        if self.selected_curve == None:
            msg.showerror('Error', 'The name of the curve is required.')
        else:
            Curve.dic[str(self.selected_curve)].name = self.active_curve_name.get()
            # Update curve data types
            self.active_curve_x_data.set(Curve.dic[str(self.selected_curve)].data_type['x_type'])
            self.active_curve_y_data.set(Curve.dic[str(self.selected_curve)].data_type['y_type'])
            # Update curve visibility
            Curve.dic[str(self.selected_curve)].visibility = self.show_state.get()
            # Update curve width
            try:
                if float(self.curve_width.get()) != 0:
                    Curve.dic[str(self.selected_curve)].width = float(self.curve_width.get())
                else:
                    # status message will be replaced by the one from 'plot_curves'.
                    msg.showerror('Error', 'The width of curve line cannot be 0.')
            except ValueError:
                msg.showerror('Error', 'The width of curve line must be a number.')
            # Update scale and offset values for curve
            try:
                if float(self.curve_x_scale.get()) != 0:
                    Curve.dic[str(self.selected_curve)].x_scale = float(self.curve_x_scale.get())
                    Curve.dic[str(self.selected_curve)].x_offset = float(self.curve_x_offset.get())
                    Curve.dic[str(self.selected_curve)].data_out.iloc[:, 0] = Curve.dic[str(self.selected_curve)].data_in.iloc[:, 0]* Curve.dic[str(self.selected_curve)].x_scale + Curve.dic[str(self.selected_curve)].x_offset
                else:
                    # status message will be replaced by the one from 'plot_curves'.
                    msg.showerror('Error', 'The value of X scale cannot be 0.')
                if float(self.curve_y_scale.get()) != 0:
                    Curve.dic[str(self.selected_curve)].y_scale = float(self.curve_y_scale.get())
                    Curve.dic[str(self.selected_curve)].y_offset = float(self.curve_y_offset.get())
                    Curve.dic[str(self.selected_curve)].data_out.iloc[:, 1] = Curve.dic[str(self.selected_curve)].data_in.iloc[:, 1]* Curve.dic[str(self.selected_curve)].y_scale + Curve.dic[str(self.selected_curve)].y_offset
                else:
                    # status message will be replaced by the one from 'plot_curves'.
                    msg.showerror('Error', 'The value of Y scale cannot be 0.')
            except ValueError:
                msg.showerror('Error', 'The values of X scale, X offset, Y scale and Y offset must be numbers.')

            self.plot_curves()

    def plot_curves(self):
        """ Plot all curves with visibility = True

            Each curve attribute is scanned and used in plot function.
            It is necessary to clear the Axes since the for loop starts from 1 for every
            curve plot. Otherwise the first curve get duplicated for each plot to this function.
            Plot annotation if required and plot its arrow if required.
            Empty main title, X title and Y titles are accepted.
        """
        self.ax.clear()
        # Set the plot windows with user-defined ranges if required.
        if self.autoscale.get():
            try:
                self.ax.axis([float(self.x_min_range.get()),
                              float(self.x_max_range.get()),
                              float(self.y_min_range.get()),
                              float(self.y_max_range.get())]
                            )
            except ValueError:
                msg.showerror('Error', 'The values of X min, X max, Y min and Y max must be numbers.')
    
        # Update curve parameters for all curves.
        for i in range(1, Curve.count+1):
            # print('Visibility ', Curve.dic[str(i)].name, Curve.dic[str(i)].visibility)
            #if Curve.dic[str(i)].data_out != None:
            # Curve data is computed again in case the curve are plot after reading a session file.
            Curve.dic[str(i)].data_out.iloc[:, 0] = Curve.dic[str(i)].data_in.iloc[:, 0]* Curve.dic[str(i)].x_scale + Curve.dic[str(i)].x_offset
            Curve.dic[str(i)].data_out.iloc[:, 1] = Curve.dic[str(i)].data_in.iloc[:, 1]* Curve.dic[str(i)].y_scale + Curve.dic[str(i)].y_offset
            if Curve.dic[str(i)].visibility:
                self.ax.plot(Curve.dic[str(i)].data_out.iloc[:, 0],
                             Curve.dic[str(i)].data_out.iloc[:, 1],
                             label=Curve.dic[str(i)].name,
                             color=Curve.dic[str(i)].color,
                             lw=Curve.dic[str(i)].width,
                             ls=Curve.dic[str(i)].style,
                             )
                # This message is not visible unless the plotting takes a long time.
                self.set_status(Curve.dic[str(i)].name+' is plotted.')

        # Draw the annotation and the arrow
        try:
            if self.annot_state.get() & self.arrow_state.get():
                self.ax.annotate(self.annotation.get(),
                        xy=(float(self.arrow_head_x.get()), float(self.arrow_head_y.get())),
                        xytext=(float(self.annotation_x.get()), float(self.annotation_y.get())),
                        color=self.annot_color_combo.get(),
                        fontsize=float(self.annot_size.get()),
                        arrowprops=dict(color=self.arrow_color_combo.get(),
                                        width=float(self.arrow_width.get()),
                                        headwidth=float(self.arrow_head_width.get()),
                                        headlength=float(self.arrow_head_length.get())
                                       )
                        )
            # Draw the annotation only. The arrowprops is removed to avoid drawing it
            elif self.annot_state.get() & (not self.arrow_state.get()):
                self.ax.annotate(self.annotation.get(),
                        xy=(float(self.arrow_head_x.get()), float(self.arrow_head_y.get())),
                        xytext=(float(self.annotation_x.get()), float(self.annotation_y.get())),
                        color=self.annot_color_combo.get(),
                        fontsize=float(self.annot_size.get()),
                        )
            # Draw no annotation and no arrow
            else:
                pass
        except ValueError:
            message1 = 'For the annotation, the values of X and Y positions and the value of font size must be numbers.'
            message2 = '\nFor the arrow, the values of X and Y positions, the length and width of head and the line width must be numbers.'
            msg.showerror('Error', message1 + message2)

        # Set the number of bins (axis ticks). Abs() is used to handle negative integers.
        try:
            self.ax.xaxis.set_major_locator(MaxNLocator(abs(int(self.x_bin.get()))+1))
            self.ax.yaxis.set_major_locator(MaxNLocator(abs(int(self.y_bin.get()))+1))
        except ValueError:
            message3 = 'The values of number of ticks for X and Y axis must be integers.'
            message4 = '\n.'
            msg.showerror('Error', message3 + message4)

        # PLOT AREA PARAMETERS
        # Background colors
        self.fig.set_facecolor(my_colors[self.plot_fig_color][0])
        self.ax.set_facecolor(my_colors[self.plot_fig_color][0])
        # Axis and label colors
        self.ax.tick_params(axis='both', color=my_colors[self.plot_fig_color][1], labelcolor=my_colors[self.plot_fig_color][1])
        # Spine color
        self.ax.spines['top'].set_color(my_colors[self.plot_fig_color][1])
        self.ax.spines['bottom'].set_color(my_colors[self.plot_fig_color][1])
        self.ax.spines['left'].set_color(my_colors[self.plot_fig_color][1])
        self.ax.spines['right'].set_color(my_colors[self.plot_fig_color][1])

        self.ax.legend(loc=self.legend_var[str(self.legend.get())])
        self.ax.set_title(self.main_title.get(), color=my_colors[self.plot_fig_color][1], fontweight='bold')
        self.ax.set_xlabel(self.x_title.get(), color=my_colors[self.plot_fig_color][1])
        self.ax.set_ylabel(self.y_title.get(), color=my_colors[self.plot_fig_color][1])
        self.ax.grid(self.grid_state.get())
        self.fig.tight_layout()
        # Update the matplotlib area. canvas.draw() will be deprecated.
        self.canvas.draw_idle()
        self.set_status('Plot is updated.')

    def active_curve(self, event):
        """ Update curve widgets based on curve attributes

            This allows the user to see the curve attributes after selecting the curve ID.
        """
        # Get the curve ID through event.
        self.selected_curve = event.widget.get()
        # check for input error on curve ID
        if self.selected_curve in Curve.dic.keys():
            # Update the active curve attributes.
            self.active_curve_name.set(Curve.dic[str(self.selected_curve)].name)
            self.show_state.set(Curve.dic[str(self.selected_curve)].visibility)
            self.active_curve_name.set(Curve.dic[str(self.selected_curve)].name)
            self.active_curve_x_data.set(Curve.dic[str(self.selected_curve)].data_type['x_type'])
            self.active_curve_y_data.set(Curve.dic[str(self.selected_curve)].data_type['y_type'])
            self.curve_color_combo.set(Curve.dic[str(self.selected_curve)].color)
            self.curve_width.set(Curve.dic[str(self.selected_curve)].width)
            self.curve_style_combo.set(Curve.dic[str(self.selected_curve)].style)
            self.curve_x_scale.set(Curve.dic[str(self.selected_curve)].x_scale)
            self.curve_y_scale.set(Curve.dic[str(self.selected_curve)].y_scale)
            self.curve_x_offset.set(Curve.dic[str(self.selected_curve)].x_offset)
            self.curve_y_offset.set(Curve.dic[str(self.selected_curve)].y_offset)
            self.set_status('Selected curve: '+Curve.dic[str(self.selected_curve)].name)
        else:
            print('ERROR - Curve ID not found. Please select again a curve ID.')
            self.set_status('ERROR - Curve ID not found. Please select again a curve ID.')

    def show_check_update(self):
        """ Process the 'show' check toggle for curve visibility."""
        try:
            Curve.dic[self.selected_curve].visibility = self.show_state.get()
            # 'plot_curves' should not be in try so that it is not launched in case of Exception.
            # This allows to have the warning message persistent in status bar.
        except AttributeError:
            self.set_status('ERROR - There is no curve defined.')

    def change_curve_color(self, event):
        """ Update the curve attribute with the selected color from combobox through event."""
        try:
            Curve.dic[str(self.selected_curve)].color = event.widget.get()
            self.set_status('Color of curve ' +
                            Curve.dic[str(self.selected_curve)].name +
                            ' is updated.'
                            )
        except AttributeError:
            self.set_status('ERROR - There is no color defined.')

    def change_curve_style(self, event):
        """ Update the curve attribute with the selected line style from combobox through event."""
        try:
            Curve.dic[str(self.selected_curve)].style = event.widget.get()
            self.set_status('Style of curve ' +
                            Curve.dic[str(self.selected_curve)].name +
                            ' is updated.'
                            )
        except AttributeError:
            self.set_status('ERROR - There is no style defined.')

    def plot_tab(self):
        """ Second tab managing plot area parameters.

            Label variables are local variables so no 'self' prepend.
        """
        # Create plot tab
        self.plot_tab = ttk.Frame(self.tool_notebook)
        # Allow the column to expand for children
        self.plot_tab.columnconfigure(index=0, weight=1)

        # TITLE PANEL
        self.plot_frame = ttk.LabelFrame(self.plot_tab, text='Plot titles')
        self.plot_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                                     padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY)
        # Allow the column to expand for children
        for i in range(0, 4):
            self.plot_frame.columnconfigure(index=i, weight=1)
        # Main title
        main_title_label = ttk.Label(self.plot_frame, text='Main title'
                )
        main_title_label.grid(row=0, column=0)
        # main_title_label.configure(anchor='center')
        self.main_title = tk.StringVar()
        self.main_title.set('Title')
        ttk.Entry(self.plot_frame, textvariable=self.main_title, width=30,
                 justify=tk.CENTER).grid(row=0, column=1)
        # X axis title
        x_title_label = ttk.Label(self.plot_frame, text='X title'
                )
        x_title_label.grid(row=1, column=0)
        self.x_title = tk.StringVar()
        self.x_title.set('X_data (units)')
        ttk.Entry(self.plot_frame, textvariable=self.x_title, width=30,
                 justify=tk.CENTER).grid(row=1, column=1)
        # Y axis title
        y_title_label = ttk.Label(self.plot_frame, text='Y title'
                )
        y_title_label.grid(row=2, column=0)
        self.y_title = tk.StringVar()
        self.y_title.set('Y_data (units)')
        ttk.Entry(self.plot_frame, textvariable=self.y_title, width=30,
                 justify=tk.CENTER).grid(row=2, column=1)

        # RANGE PANEL
        self.range_frame = ttk.LabelFrame(self.plot_tab, text='Plot ranges for X and Y')
        self.range_frame.grid(row=1, column=0)
        # Allow the column to expand for children
        for i in range(0, 4):
            self.range_frame.columnconfigure(index=i, weight=1)
        # Auto-scale or user defined
        self.autoscale = tk.IntVar()
        self.autoscale.set(0)
        ttk.Radiobutton(self.range_frame, text='Auto scale', variable=self.autoscale,
                       value=0, command=self.update_user_state).grid(row=0, column=0, columnspan=2)

        ttk.Radiobutton(self.range_frame, text='User defined', variable=self.autoscale,
                       value=1, command=self.update_user_state).grid(row=0, column=2, columnspan=2)
        # User defined
        ttk.Label(self.range_frame, text='User defined ranges:'
                ).grid(row=1, column=0, columnspan=2)
    
        # X min
        x_min_label = ttk.Label(self.range_frame, text='X min'
                )
        x_min_label.grid(row=2, column=0)
        # x_min_label.configure(anchor='center')
        self.x_min_range = tk.StringVar()
        self.x_min_range.set('0')
        self.x_min_entry = ttk.Entry(self.range_frame, textvariable=self.x_min_range, width=8,
                 justify=tk.CENTER)
        self.x_min_entry.configure(state='disabled')
        self.x_min_entry.grid(row=2, column=1)
        # Y min
        y_min_label = ttk.Label(self.range_frame, text='Y min'
                )
        y_min_label.grid(row=2, column=2)
        # y_min_label.configure(anchor='center')
        self.y_min_range = tk.StringVar()
        self.y_min_range.set('0')
        self.y_min_entry = ttk.Entry(self.range_frame, textvariable=self.y_min_range, width=8, 
                 justify=tk.CENTER)
        self.y_min_entry.configure(state='disabled')
        self.y_min_entry.grid(row=2, column=3)
        # X max
        x_max_label = ttk.Label(self.range_frame, text='X max'
                )
        x_max_label.grid(row=3, column=0)
        # x_max_label.configure(anchor='center')
        self.x_max_range = tk.StringVar()
        self.x_max_range.set('100')
        self.x_max_entry = ttk.Entry(self.range_frame, textvariable=self.x_max_range, width=8, 
                 justify=tk.CENTER)
        self.x_max_entry.configure(state='disabled')
        self.x_max_entry.grid(row=3, column=1)
        # Y max
        y_max_label = ttk.Label(self.range_frame, text='Y max'
                )
        y_max_label.grid(row=3, column=2)
        # y_max_label.configure(anchor='center')
        self.y_max_range = tk.StringVar()
        self.y_max_range.set('100')
        self.y_max_entry = ttk.Entry(self.range_frame, textvariable=self.y_max_range, width=8, 
                 justify=tk.CENTER)
        self.y_max_entry.configure(state='disabled')
        self.y_max_entry.grid(row=3, column=3)

        # Tick label
        ttk.Label(self.range_frame, text='Numbers of ticks:'
                ).grid(row=4, column=0, columnspan=2)
        # X tick
        x_tick_label = ttk.Label(self.range_frame, text='X axis'
                )
        x_tick_label.grid(row=5, column=0)
        # x_tick_label.configure(anchor='center')
        self.x_bin = tk.StringVar()
        self.x_bin.set('10')
        ttk.Entry(self.range_frame, textvariable=self.x_bin, width=8,
                 justify=tk.CENTER).grid(row=5, column=1)
        # Y tick
        y_tick_label = ttk.Label(self.range_frame, text='Y axis'
                )
        y_tick_label.grid(row=5, column=2)
        # y_tick_label.configure(anchor='center')
        self.y_bin = tk.StringVar()
        self.y_bin.set('10')
        ttk.Entry(self.range_frame, textvariable=self.y_bin, width=8,
                 justify=tk.CENTER).grid(row=5, column=3)

        # LEGEND PANEL
        self.legend_frame = ttk.LabelFrame(self.plot_tab, text='Legend position')
        self.legend_frame.grid(row=2, column=0)
        # Allow the column to expand for children
        for i in range(0, 2):
            self.legend_frame.columnconfigure(index=i, weight=1)
        temp = "'Best' lets matplotlib decide the position."
        ttk.Label(self.legend_frame, text=temp
                ).grid(row=0, column=0, columnspan=3)
        # Legend position
        self.legend = tk.IntVar()
        self.legend.set(4)
        ttk.Radiobutton(self.legend_frame, text='Upper left', variable=self.legend, value=0
                      ).grid(row=1, column=0)
        ttk.Radiobutton(self.legend_frame, text='Upper right', variable=self.legend, value=1
                      ).grid(row=1, column=1)
        ttk.Radiobutton(self.legend_frame, text='Lower left', variable=self.legend, value=2
                      ).grid(row=2, column=0)
        ttk.Radiobutton(self.legend_frame, text='Lower right', variable=self.legend, value=3
                      ).grid(row=2, column=1)
        ttk.Radiobutton(self.legend_frame, text='Best', variable=self.legend, value=4
                      ).grid(row=1, column=2)
        self.legend_var ={'0': 'upper left',
                          '1': 'upper right',
                          '2': 'lower left',
                          '3': 'lower right',
                          '4': 'best'
                         }

        # CUSTOMIZE PANEL
        self.custom_frame = ttk.LabelFrame(self.plot_tab, text='Customize plot')
        self.custom_frame.grid(row=3, column=0)

        # Background color 
        x_min_label = ttk.Label(self.custom_frame, text='Background color'
                )
        x_min_label.grid(row=0, column=0, columnspan=2)
        # x_min_label.configure(anchor='center')
        # Matplotlib global color setting
        self.fig_color_flag = tk.IntVar()
        self.fig_color_flag.set(0)
        ttk.Radiobutton(self.custom_frame, text='White', variable=self.fig_color_flag,
        				value=0, command=self.update_plot_bg_color
                      ).grid(row=0, column=2)
        ttk.Radiobutton(self.custom_frame, text='Black', variable=self.fig_color_flag, 
        				value=1, command=self.update_plot_bg_color
                      ).grid(row=0, column=3)
        # Show grid
        self.grid_state = tk.IntVar()
        self.grid_state.set(1)
        ttk.Checkbutton(self.custom_frame, text='Show grid', variable=self.grid_state
                      ).grid(row=1, column=0)

        # APPLY BUTTON
        # Padding for apply needs to be the same for containers for layout consistency
        ttk.Button(self.plot_tab, text='Apply plot properties', command=self.plot_curves
                 ).grid(row=4, column=0)

        # APPLY PADDING AND STICKINESS ON WIDGETS CHILDREN AFTER THEY ARE CREATED
        # For self.plot_tab frame
        for frame in self.plot_tab.winfo_children():
            frame.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S,
                                 padx=self.CONTAINER_PADX, 
                                 pady=self.CONTAINER_PADY
                                )
        # For self.plot_frame, self.range_frame,  frames
        union_list = (set(self.plot_frame.winfo_children()) |
                      set(self.range_frame.winfo_children()) |
                      set(self.legend_frame.winfo_children()) |
                      set(self.custom_frame.winfo_children())
                     )
        for widget in union_list:
            widget.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S, 
                                  padx=self.WIDGET_PADX, 
                                  pady=self.WIDGET_PADY
                                 )

        # Add this tab to the notebook.
        self.tool_notebook.add(self.plot_tab, text='Plot area')

    def update_user_state(self):
        """necessary to update the state of ttk entries for user defined ranges"""
        if self.autoscale.get() == 0:
            self.x_min_entry.configure(state='disabled')
            self.x_max_entry.configure(state='disabled')
            self.y_min_entry.configure(state='disabled')
            self.y_max_entry.configure(state='disabled')
        else:
            self.x_min_entry.configure(state='normal')
            self.x_max_entry.configure(state='normal')
            self.y_min_entry.configure(state='normal')
            self.y_max_entry.configure(state='normal')

    def annotation_tab(self):
        """ Third tab managing annotations.

            Label variables are local variables so no 'self' prepend.
        """
        # Create annotation tab
        self.annot_tab = ttk.Frame(self.tool_notebook)
        # Allow the column to expand for children
        self.annot_tab.columnconfigure(index=0, weight=1)

        # Comment
        ttk.Label(self.annot_tab, text='X and Y positions refer to data coordinate system.',
                 justify=tk.LEFT).grid(row=0, column=0)
    
        # TEXT PANEL
        self.text_frame = ttk.LabelFrame(self.annot_tab, text='Annotation')
        self.text_frame.grid(row=1, column=0)
        # Allow the column to expand for children
        for i in range(0, 4):
            self.text_frame.columnconfigure(index=i, weight=1)
        # Text
        text_label = ttk.Label(self.text_frame, text='Text'
                )
        text_label.grid(row=0, column=0)
        # text_label.configure(anchor='center')
        self.annotation = tk.StringVar()
        self.annotation.set('Annotation_text')
        ttk.Entry(self.text_frame, textvariable=self.annotation, width=30,
                 justify=tk.CENTER).grid(row=0, column=1, columnspan=3)
        # X position of annotation
        text_x_pos_label = ttk.Label(self.text_frame, text='X position'
                )
        text_x_pos_label.grid(row=1, column=0)
        # text_x_pos_label.configure(anchor='center')
        self.annotation_x = tk.StringVar()
        self.annotation_x.set('0')
        ttk.Entry(self.text_frame, textvariable=self.annotation_x, width=8,
                 justify=tk.CENTER).grid(row=1, column=1)
        # Y position of annotation
        text_y_pos_label = ttk.Label(self.text_frame, text='Y position'
                )
        text_y_pos_label.grid(row=1, column=2)
        # text_y_pos_label.configure(anchor='center')
        self.annotation_y = tk.StringVar()
        self.annotation_y.set('0')
        ttk.Entry(self.text_frame, textvariable=self.annotation_y, width=8,
                 justify=tk.CENTER).grid(row=1, column=3)
        # Color
        text_color_label = ttk.Label(self.text_frame, text='Text color'
                )
        text_color_label.grid(row=2, column=0)
        # text_color_label.configure(anchor='center')
        self.annot_color_combo = ttk.Combobox(self.text_frame,
                                              values=my_colors[self.plot_fig_color],
                                              justify=tk.CENTER,
                                              width=8
                                             )
        self.annot_color_combo.set(my_colors[self.plot_fig_color][1])
        self.annot_color_combo.grid(row=2, column=1)
        # Binding the callback to self.arrow_color_combo is not necessary si 'apply all' will get the color value.
        # Font size
        font_size_label = ttk.Label(self.text_frame, text='Font size'
                )
        font_size_label.grid(row=2, column=2)
        # font_size_label.configure(anchor='center')
        self.annot_size = tk.StringVar()
        self.annot_size.set('10')
        ttk.Entry(self.text_frame, textvariable=self.annot_size, width=8,
                 justify=tk.CENTER).grid(row=2, column=3)
        # Show annotation
        self.annot_state = tk.IntVar()
        self.annot_state.set(0)
        # No callback since 'Apply all' redraw the plot with or without the annotation.
        ttk.Checkbutton(self.text_frame, text='Show the annotation on the plot', variable=self.annot_state
                       ).grid(row=3, column=0, columnspan=4)
        
        # ARROW PANEL
        self.arrow_frame = ttk.LabelFrame(self.annot_tab, text='Arrow properties')
        self.arrow_frame.grid(row=3, column=0,  columnspan=2)
        # Allow the column to expand for children
        for i in range(0, 4):
            self.arrow_frame.columnconfigure(index=i, weight=1)
        # X position of arrow head
        head_x_pos_label = ttk.Label(self.arrow_frame, text='Head X pos.'
                )
        head_x_pos_label.grid(row=0, column=0)
        # head_x_pos_label.configure(anchor='center')
        self.arrow_head_x = tk.StringVar()
        self.arrow_head_x.set('0')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_x, width=8,
                 justify=tk.CENTER).grid(row=0, column=1)
        # Y position of arrow head
        head_y_pos_label = ttk.Label(self.arrow_frame, text='Head Y pos.'
                )
        head_y_pos_label.grid(row=0, column=2)
        # head_y_pos_label.configure(anchor='center')
        self.arrow_head_y = tk.StringVar()
        self.arrow_head_y.set('0')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_y, width=8,
                 justify=tk.CENTER).grid(row=0, column=3)
        # Length of arrow head
        head_length_label = ttk.Label(self.arrow_frame, text='Head length'
                )
        head_length_label.grid(row=1, column=0)
        # head_length_label.configure(anchor='center')
        self.arrow_head_length = tk.StringVar()
        self.arrow_head_length.set('10')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_length, width=8,
                 justify=tk.CENTER).grid(row=1, column=1)
        # Width of arrow head
        head_width_label = ttk.Label(self.arrow_frame, text='Head width'
                )
        head_width_label.grid(row=1, column=2)
        # head_width_label.configure(anchor='center')
        self.arrow_head_width = tk.StringVar()
        self.arrow_head_width.set('4')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_width, width=8,
                 justify=tk.CENTER).grid(row=1, column=3)
        # Color of arrow
        line_color_label = ttk.Label(self.arrow_frame, text='Line color')
        line_color_label.grid(row=2, column=0)
        # line_color_label.configure(anchor='center')
        self.arrow_color_combo = ttk.Combobox(self.arrow_frame,
                                                values=my_colors[self.plot_fig_color],
                                                justify=tk.CENTER,
                                                width=8
                                                )
        self.arrow_color_combo.set(my_colors[self.plot_fig_color][1])
        self.arrow_color_combo.grid(row=2, column=1)
        # Binding the callback to self.arrow_color_combo is not necessary si 'apply all' will get the color value.
        # Width of arrow
        line_width_label = ttk.Label(self.arrow_frame, text='Line width'
                )
        line_width_label.grid(row=2, column=2)
        # line_width_label.configure(anchor='center')
        self.arrow_width = tk.StringVar()
        self.arrow_width.set('0.5')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_width, width=8,
                 justify=tk.CENTER).grid(row=2, column=3)
        # Show arrow.
        self.arrow_state = tk.IntVar()
        self.arrow_state.set(0)
        # No callback since 'Apply all' redraw the plot with or without the annotation.
        ttk.Checkbutton(self.arrow_frame, variable=self.arrow_state,
                        text='Show the arrow connected to the annotation'
                       ).grid(row=5, column=0, columnspan=4)

        # APPLY BUTTON
        # Padding for apply needs to be the same for containers for layout consistency
        ttk.Button(self.annot_tab, text='Apply annotation and arrow properties',
                  command=self.plot_curves, style='w6.TButton').grid(row=4, column=0)

        # APPLY PADDING AND STICKINESS ON WIDGETS CHILDREN AFTER THEY ARE CREATED
        # For self.annot_tab
        for frame in self.annot_tab.winfo_children():
            frame.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S,
                                 padx=self.CONTAINER_PADX, 
                                 pady=self.CONTAINER_PADY
                                )
        # For all frames
        union_list = (set(self.text_frame.winfo_children()) |
                      set(self.arrow_frame.winfo_children())
                     )
        for widget in union_list:
            widget.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S, 
                                  padx=self.WIDGET_PADX, 
                                  pady=self.WIDGET_PADY
                                 )

        # Add this tab to the notebook.
        self.tool_notebook.add(self.annot_tab, text='Annotation')

    def extrema_tab(self):
        """ Fourth tab managing extrema.

            Label variables are local variables so no 'self' prepend.
        """
        # Create extrema tab
        self.extrema_tab = ttk.Frame(self.tool_notebook)
        # Allow the column to expand for children
        self.extrema_tab.columnconfigure(index=0, weight=1)

        # Label
        txt = 'Values are rounded with ' + str(self.ROUND) + ' digits after decimal.'
        comment = ttk.Label(self.extrema_tab, text=txt)
        comment.grid(row=0, column=0, columnspan=4)
        comment.configure(anchor=tk.W)
        # Active curve selection
        select_curve_label2 = ttk.Label(self.extrema_tab, text='Select curve')
        select_curve_label2.grid(row=1, column=0)
        # select_curve_label2.configure(anchor='center')
        self.active_curve_combo2 = ttk.Combobox(self.extrema_tab,
                                               values=list(Curve.dic.keys()),
                                               justify=tk.CENTER,
                                               width=4,
                                               )
        self.active_curve_combo2.grid(row=1, column=1)
        self.active_curve_combo2.bind('<<ComboboxSelected>>', self.get_extrema)
        # Label
        selected_curve_label = ttk.Label(self.extrema_tab, text='Curve name')
        selected_curve_label.grid(row=1, column=2)
        # selected_curve_label.configure(anchor='center')
        # Entry for curve name
        self.selected_curve_name = tk.StringVar()
        self.selected_curve_name.set(' ')
        ttk.Entry(self.extrema_tab, textvariable=self.selected_curve_name, width=20,
                 justify=tk.CENTER).grid(row=1, column=3)
        # Xmin
        self.extrema_x_min = tk.StringVar()
        self.extrema_x_min.set('X min')
        extrema_x_min_label = ttk.Label(self.extrema_tab, textvariable=self.extrema_x_min)
        extrema_x_min_label.grid(row=3, column=0, columnspan=4)
        # Xmax
        self.extrema_x_max = tk.StringVar()
        self.extrema_x_max.set('X max')
        extrema_x_max_label = ttk.Label(self.extrema_tab, textvariable=self.extrema_x_max)
        extrema_x_max_label.grid(row=4, column=0, columnspan=4)
        # Ymin
        self.extrema_y_min = tk.StringVar()
        self.extrema_y_min.set('Y min')
        extrema_y_min_label = ttk.Label(self.extrema_tab, textvariable=self.extrema_y_min)
        extrema_y_min_label.grid(row=5, column=0, columnspan=4)
        # Ymax
        self.extrema_y_max = tk.StringVar()
        self.extrema_y_max.set('Y max')
        extrema_y_max_label = ttk.Label(self.extrema_tab, textvariable=self.extrema_y_max)
        extrema_y_max_label.grid(row=6, column=0, columnspan=4)

        # For all frames
        union_list = (set(self.extrema_tab.winfo_children()) 
                     )
        for widget in union_list:
            widget.grid_configure(sticky=tk.E+tk.W+tk.N+tk.S, 
                                  padx=self.WIDGET_PADX, 
                                  pady=self.WIDGET_PADY
                                 )

        # Add this tab to the notebook.
        self.tool_notebook.add(self.extrema_tab, text='Extrema')

    def get_extrema(self, event):
        # Get the curve ID through event.
        selected_curve2 = event.widget.get()
        # check for input error on curve ID
        if selected_curve2 in Curve.dic.keys():
            # show the curve name after selection of curve ID
            self.selected_curve_name.set(Curve.dic[str(selected_curve2)].name)
            Curve.dic[str(selected_curve2)].find_extrema()
            self.set_status('Extrema values computed for curve: ' + Curve.dic[str(selected_curve2)].name)
        else:
            print('ERROR - Curve ID not found. Please select again a curve ID.')
            self.set_status('ERROR - Curve ID not found. Please select again a curve ID.')

    def update_plot_bg_color(self):
    	if self.fig_color_flag.get() == 0:
    		self.plot_fig_color = 'white_bg'
    	elif self.fig_color_flag.get() == 1:
    		self.plot_fig_color = 'black_bg'


if __name__ == '__main__':
    app = Application()
    # Show the screen dimensions at start-up.
    """
    screen_height = app.winfo_screenheight()
    screen_width = app.winfo_width()
    print('Screen height', screen_height)
    print('Screen width', screen_width)
    """
    # Define the min size for the window. It should be enough even for old screens.
    app.minsize(800, 610)
    # Launch the GUI mainloop which should always be the last instruction!
    app.mainloop()
