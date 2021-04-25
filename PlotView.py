# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    PlotView is summarized as PV in variable names.
"""


try:
    from collections import OrderedDict
    import configparser
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
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
my_colors_white = ['black', 'grey', 'red', 'darksalmon', 'sienna', 'tan', 'gold',
             'green', 'dodgerblue', 'blueviolet', 'hotpink', 'orange',
             'peru', 'limegreen', 'turquoise', 'royalblue'
             ]
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
        self.name = 'Name'
        self.path = path
        self.data_in = self.read_file(path)
        self.data_type = {'x_type': self.data_in.columns[0], 'y_type': self.data_in.columns[1]}
        self.data_out = self.data_in.copy()
        self.visibility = True
        self.color = my_colors_white[0]
        self.width = 1.0
        self.style = my_linestyles[0]
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.x_scale = 1.0
        self.y_scale = 1.0
        Curve.count += 1

    def read_file(self, path):
        """ Read the curve CSV file.

            It is necessary to convert data to float in 'read_csv' in order to plot.
            Requirements on the file format:
                - delete unused data and headers: header should be on the first line
                - rename column headers if necessary
                - only 2 columns of data
                - make sure that comma is the delimiter
                - decimal character is the point '.'
        """
        df = pd.read_csv(self.path, delimiter=',', dtype=float)
        return df
        # TODO: handle following exceptions: no column, 1 column, more than 2 columns, strings, missing values, etc.


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

            Methods: they launch the window layout setup, and create the tab on the RH side for tools.
        """
        super().__init__()

        # ATTRIBUTES
        # Main window parameters.
        self.PV_VERSION = '0.13'
        self.WIN_RESIZABLE = False
        self.WIN_SIZE_POS = '1280x720+0+0'
        self.FONT_SIZE = 9
        # Matplotlib parameters.
        self.PLOT_WIDTH = 8.9
        self.PLOT_HEIGHT = 6.68
        # Parameters for widgets on RH tool panel.
        # Padding for all containers to uniformize the look
        self.CONTAINER_PADX = 6
        self.CONTAINER_PADY = 6
        # Padding for all widgets inside a container
        self.WIDGET_PADX = 2
        self.WIDGET_PADY = 2
        # Max length of string showed by 'Create curve' labels.
        # This is related to window width, font, and font size.
        self.MAX_STR_CREATE_CURVE = 35

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

        # MENUS
        menu_main = tk.Menu(self)
        # Menu tear off is disabled.
        menu_file = tk.Menu(menu_main, tearoff='False')
        menu_help = tk.Menu(menu_main, tearoff='False')
        # Add menu_file in menu_main
        menu_main.add_cascade(label='File', menu=menu_file)
        menu_main.add_cascade(label='Help', menu=menu_help)
        # Link of main menu to root window
        self.config(menu=menu_main)
        # File Menu
        menu_file.add_command(label='Load PV_session.ini', command=self.load_session)
        menu_file.add_command(label='Save PV_session.ini', command=self.save_session)
        menu_file.add_command(label='Quit', command=self.app_quit)
        # Help Menu
        menu_help.add_command(label='Help on PlotView', command=self.help_redirect)
        menu_help.add_command(label='Licence GPLv3', command=self.licence_redirect)
        menu_help.add_command(label='About', command=self.about_redirect)

        # CREATE STATUS BAR AT BOTTOM
        self.status_frame = tk.Frame(self)
        # The status frame should extend on all width of the main window.
        self.status_frame.pack(expand=False, fill=tk.X, side=tk.BOTTOM)
        # The status is initialized with empty message left aligned.
        self.status = tk.Label(self.status_frame,
                               text=' Ready.',
                               bd=1,
                               relief=tk.SUNKEN,
                               anchor=tk.W,
                               padx=self.WIDGET_PADX,
                               pady=self.WIDGET_PADY
                               )
        # The label shoul expand on the total window width.
        self.status.pack(fill=tk.BOTH, expand=False)

        # CREATE PLOT AREA ON THE LEFT
        # Tip: https://stackoverflow.com/questions/29432683/resizing-a-matplotlib-plot-in-a-tkinter-toplevel
        self.fig = plt.Figure(figsize=(self.PLOT_WIDTH, self.PLOT_HEIGHT))
        self.ax = self.fig.add_subplot(111)
        self.mat_frame = ttk.Frame(self)
        self.mat_frame.pack(expand=False, side=tk.LEFT)
        # Creates a drawing area to put the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mat_frame)
        self.canvas.draw()
        # Creates the Matplotlib navigation tool bar for figures.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.mat_frame)
        self.toolbar.draw()
        self.canvas.get_tk_widget().pack()

        # CREATE A NOTEBOOK ON THE RIGHT FOR TOOL WIDGETS
        # Frame for RH panel. It contains the ttk.notebook.
        self.tool_frame = ttk.Frame(self)
        self.tool_frame.pack(expand=True, fill=tk.BOTH)
        # Notebook
        self.tool_notebook = ttk.Notebook(self.tool_frame)
        self.tool_notebook.pack(expand=True, fill=tk.BOTH)

    def app_quit(self):
        """ Quit the application and free the stack."""
        self.destroy()
        sys.exit(0)

    def help_redirect(self):
        """ Plotview HTML help is shown in web browser."""
        webbrowser.open_new_tab('help/index.html')
        self.set_status('The PlotView help page is shown in your web browser.')

    def licence_redirect(self):
        """ PlotView licence is shown in the text editor."""
        webbrowser.open_new_tab('LICENSE')
        self.set_status('The GPL3 licence is now opened.')

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
                          'legend position': self.legend.get(),
                          'display grid': self.grid_state.get()
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
        with open('PV_session.ini', 'w') as file:
            config.write(file)
        self.set_status('Session file "PV_session.ini" is written where PlotView.py file is located.')

    def load_session(self):
        """ Load session file
        
            Curve data are read.
            Plot data are read.
        """
        config = configparser.ConfigParser()
        # TODO: Show a warning or ask a permission since the work will be lost ?
        # Read the file
        config.read('PV_session.ini')
        # Process Plot section
        self.main_title.set(config.get('plot', 'main title'))
        self.x_title.set(config.get('plot', 'x title'))
        self.y_title.set(config.get('plot', 'y title'))
        self.autoscale.set(config.getboolean('plot', 'auto scale'))
        self.x_min_range.set(config.get('plot', 'x min user range'))
        self.x_max_range.set(config.get('plot', 'x max user range'))
        self.y_min_range.set(config.get('plot', 'y min user range'))
        self.y_max_range.set(config.get('plot', 'y max user range'))
        self.legend.set(config.getint('plot', 'legend position'))
        self.grid_state.set(config.getboolean('plot', 'display grid'))
        self.main_title.set(config.get('plot', 'main title'))
        self.main_title.set(config.get('plot', 'main title'))
        self.main_title.set(config.get('plot', 'main title'))
        self.main_title.set(config.get('plot', 'main title'))

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



    def curve_tab(self):
        """ First tab managing curve creation."""
        # Create curve tab
        self.curve_tab = ttk.Frame(self.tool_notebook)

        # CREATE CURVE PANEL
        self.create_curve_frame = ttk.LabelFrame(self.curve_tab, text='Create curve')
        self.create_curve_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                                     padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                                    )
        # Working directory widgets
        ttk.Button(self.create_curve_frame, text='Work dir.',
                  command=self.choose_dir, width=9
                  ).grid(row=0, column=0,
                         padx=self.WIDGET_PADX,
                         pady=self.WIDGET_PADY
                        )
        ttk.Label(self.create_curve_frame,
                 textvariable=self.work_dir_txt
                 ).grid(row=0, column=1,
                        padx=self.WIDGET_PADX,
                        pady=self.WIDGET_PADY)
        # CSV file widget
        ttk.Button(self.create_curve_frame, text='CSV file',
                  command=self.choose_file, width=9
                 ).grid(row=1, column=0,
                        padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                       )
        ttk.Label(self.create_curve_frame, textvariable=self.work_file_txt
                ).grid(row=1, column=1,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        # Curve name widget
        ttk.Label(self.create_curve_frame, text='Curve name'
                ).grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_label = tk.StringVar()
        self.curve_label.set('Curve_name')
        ttk.Entry(self.create_curve_frame, textvariable=self.curve_label, width=27,
                 justify=tk.CENTER).grid(row=2, column=1,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Curve create widget
        ttk.Button(self.create_curve_frame, text='Create',
                  command=self.curve_create, width=4
                 ).grid(row=3, column=0, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S,
                                padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                       )

        # CURVE PROPERTIES
        self.curve_prop_frame = ttk.LabelFrame(self.curve_tab, text='Curve properties')
        self.curve_prop_frame.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                                   padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                                  )
        # Active curve selection
        # Tip: https://stackoverflow.com/questions/54283975/python-tkinter-combobox-and-dictionary
        ttk.Label(self.curve_prop_frame, text='Select curve'
                ).grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.active_curve_combo = ttk.Combobox(self.curve_prop_frame,
                                               values=list(Curve.dic.keys()),
                                               justify=tk.CENTER,
                                               width=4,
                                               )
        self.active_curve_combo.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                     padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                    )
        self.active_curve_combo.bind('<<ComboboxSelected>>', self.active_curve)

        # Show curve
        self.show_state = tk.IntVar()
        self.show_state.set(1)
        ttk.Checkbutton(self.curve_prop_frame, text='Show curve',
                       variable=self.show_state
                      ).grid(row=0, column=2, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )
        # Curve Name
        self.active_curve_name = tk.StringVar()
        self.active_curve_name.set(' ')
        ttk.Label(self.curve_prop_frame, text='Name'
                ).grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        ttk.Entry(self.curve_prop_frame, textvariable=self.active_curve_name,
                 width=30, justify=tk.CENTER
                ).grid(row=1, column=1, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S,
                padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        # Curve color
        ttk.Label(self.curve_prop_frame, text='Line color'
                ).grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_color_combo = ttk.Combobox(self.curve_prop_frame,
                                                values=my_colors_white,
                                                justify=tk.CENTER,
                                                width=12
                                                )
        self.curve_color_combo.set(my_colors_white[0])
        self.curve_color_combo.grid(row=2, column=1, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S,
                                    padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                   )
        self.curve_color_combo.bind('<<ComboboxSelected>>', self.change_curve_color)
        # Line width
        ttk.Label(self.curve_prop_frame, text='Line width'
                ).grid(row=3, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_width = tk.StringVar()
        self.curve_width.set('1')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_width, width=4, justify=tk.CENTER).grid(
                  row=3, column=1, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.E+tk.W+tk.N+tk.S)
        # Line style
        ttk.Label(self.curve_prop_frame,
                text='Line style').grid(row=3,
                        column=2, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.E+tk.W+tk.N+tk.S)
        self.curve_style_combo = ttk.Combobox(self.curve_prop_frame,
                                                values=my_linestyles,
                                                justify=tk.CENTER,
                                                width=3
                                                )
        self.curve_style_combo.set(my_linestyles[0])
        self.curve_style_combo.grid(row=3, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                    padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                   )
        self.curve_style_combo.bind('<<ComboboxSelected>>', self.change_curve_style)
        # X scale
        ttk.Label(self.curve_prop_frame, text='Scale X axis'
                ).grid(row=5, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_x_scale = tk.StringVar()
        self.curve_x_scale.set('1')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_x_scale, width=8,
                 justify=tk.CENTER).grid(row=5, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        # Y scale
        ttk.Label(self.curve_prop_frame, text='Scale Y axis'
                ).grid(row=5, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_y_scale = tk.StringVar()
        self.curve_y_scale.set('1')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_y_scale, width=8,
                 justify=tk.CENTER).grid(row=5, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # X offset
        ttk.Label(self.curve_prop_frame, text='Offset X axis'
                ).grid(row=6, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_x_offset = tk.StringVar()
        self.curve_x_offset.set('0')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_x_offset, width=8,
                 justify=tk.CENTER).grid(row=6, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                         )
        # Y offset
        ttk.Label(self.curve_prop_frame, text='Offset Y axis'
                ).grid(row=6, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.curve_y_offset = tk.StringVar()
        self.curve_y_offset.set('0')
        ttk.Entry(self.curve_prop_frame, textvariable=self.curve_y_offset, width=8,
                 justify=tk.CENTER).grid(row=6, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )

        # APPLY BUTTON
        ttk.Button(self.curve_prop_frame, text='Apply',
                  command=self.update_curve, width=6
                 ).grid(row=7, column=0, columnspan=4, sticky=tk.E+tk.W+tk.N+tk.S,
                        padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
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
                # Show the name of the created curve in 'curve_label'
                Curve.dic[str(Curve.count)].name = self.curve_label.get()
                # Update the list of curve for future modifications.
                self.active_curve_combo['values'] = tuple(list(Curve.dic.keys()))
                self.plot_curves()
            else:
                msg.showerror('Error', 'The name of the curve is required.')
        else:
            msg.showerror('Error', 'No CSV file were selected.')

    def update_curve(self):
        """ Update Curve instance attributes based on GUI input"""
        # Update curve name
        if len(self.active_curve_name.get()) != 0:
            Curve.dic[str(self.selected_curve)].name = self.active_curve_name.get()
        else:
            # status message will be replaced by the one from 'plot_curves'.
            msg.showerror('Error', 'The name of the curve is required.')

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

        # Set plot area parameters
        self.ax.legend(loc=self.legend_var[str(self.legend.get())])
        self.ax.set_title(self.main_title.get(), fontweight='bold')
        self.ax.set_xlabel(self.x_title.get())
        self.ax.set_ylabel(self.y_title.get())
        self.ax.grid(self.grid_state.get())
        self.fig.tight_layout()
        # Update the matplotlib area
        self.canvas.draw()
        self.set_status('Plot is updated.')

    def active_curve(self, event):
        """ Update curve widgets based on curve attributes

            This allows the user to see the curve attributes after selecting the curve ID.
        """
        try:
            # Get the curve ID through event.
            self.selected_curve = event.widget.get()
            # Update the active curve attributes.
            self.active_curve_name.set(Curve.dic[str(self.selected_curve)].name)
            self.show_state.set(Curve.dic[str(self.selected_curve)].visibility)
            self.active_curve_name.set(Curve.dic[str(self.selected_curve)].name)
            self.curve_color_combo.set(Curve.dic[str(self.selected_curve)].color)
            self.curve_width.set(Curve.dic[str(self.selected_curve)].width)
            self.curve_style_combo.set(Curve.dic[str(self.selected_curve)].style)
            self.curve_x_scale.set(Curve.dic[str(self.selected_curve)].x_scale)
            self.curve_y_scale.set(Curve.dic[str(self.selected_curve)].y_scale)
            self.curve_x_offset.set(Curve.dic[str(self.selected_curve)].x_offset)
            self.curve_y_offset.set(Curve.dic[str(self.selected_curve)].y_offset)
            self.set_status('Selected curve: '+Curve.dic[str(self.selected_curve)].name)
        except AttributeError:
            # TODO add a warning popup window.
            self.set_status('ERROR - There is no curve defined.')

        # Get the curve ID through event.
        self.selected_curve = event.widget.get()
        print('Selected curve :', self.active_curve_combo.get())
        # check for input error on curve ID
        if self.selected_curve in Curve.dic.keys():
            # Update the active curve attributes.
            self.active_curve_name.set(Curve.dic[str(self.selected_curve)].name)
            self.show_state.set(Curve.dic[str(self.selected_curve)].visibility)
            self.active_curve_name.set(Curve.dic[str(self.selected_curve)].name)
            self.curve_color_combo.set(Curve.dic[str(self.selected_curve)].color)
            self.curve_width.set(Curve.dic[str(self.selected_curve)].width)
            self.curve_style_combo.set(Curve.dic[str(self.selected_curve)].style)
            self.curve_x_scale.set(Curve.dic[str(self.selected_curve)].x_scale)
            self.curve_y_scale.set(Curve.dic[str(self.selected_curve)].y_scale)
            self.curve_x_offset.set(Curve.dic[str(self.selected_curve)].x_offset)
            self.curve_y_offset.set(Curve.dic[str(self.selected_curve)].y_offset)
            self.set_status('Selected curve: '+Curve.dic[str(self.selected_curve)].name)
        else:
            # TODO add a warning popup window.
            print('ERROR - Curve ID not found. Please select again a curve ID.')
            self.set_status('ERROR - Curve ID not found. Please select again a curve ID.')

    def show_check_update(self):
        """ Process the 'show' check toggle for curve visibility."""
        try:
            Curve.dic[self.selected_curve].visibility = self.show_state.get()
            # 'plot_curves' should not be in try so that it is not launched in case of Exception.
            # This allows to have the warning message persistent in status bar.
        except AttributeError:
            # TODO add a error popup window.
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
            # TODO add a error popup window.
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
            # TODO add a error popup window.
            self.set_status('ERROR - There is no style defined.')

    def plot_tab(self):
        """ Second tab managing plot area parameters."""
        # Create plot tab
        self.plot_tab = ttk.Frame(self.tool_notebook)

        # TITLE PANEL
        self.plot_frame = ttk.LabelFrame(self.plot_tab, text='Plot titles')
        self.plot_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                                     padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY)
        # Main title
        ttk.Label(self.plot_frame, text='Main title'
                ).grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.main_title = tk.StringVar()
        self.main_title.set('Title')
        ttk.Entry(self.plot_frame, textvariable=self.main_title, width=30,
                 justify=tk.CENTER).grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # X axis title
        ttk.Label(self.plot_frame, text='X title'
                ).grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.x_title = tk.StringVar()
        self.x_title.set('X_data (units)')
        ttk.Entry(self.plot_frame, textvariable=self.x_title, width=30,
                 justify=tk.CENTER).grid(row=1, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Y axis title
        ttk.Label(self.plot_frame, text='Y title'
                ).grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.y_title = tk.StringVar()
        self.y_title.set('X_data (units)')
        ttk.Entry(self.plot_frame, textvariable=self.y_title, width=30,
                 justify=tk.CENTER).grid(row=2, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )

        # RANGE PANEL
        self.range_frame = ttk.LabelFrame(self.plot_tab, text='Plot ranges for X and Y')
        self.range_frame.grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                              padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                             )
        # Auto-scale or user defined
        self.autoscale = tk.IntVar()
        self.autoscale.set(0)
        ttk.Radiobutton(self.range_frame, text='Auto scale', variable=self.autoscale,
                       value=0).grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S,
                                     padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                    )
        ttk.Radiobutton(self.range_frame, text='User defined', variable=self.autoscale,
                       value=1).grid(row=0, column=2, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S,
                                     padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                    )
        # User defined
        ttk.Label(self.range_frame, text='User defined ranges:'
                ).grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        # https://stackoverflow.com/questions/26333769/event-triggered-by-listbox-and-radiobutton-in-tkinter
        # X min
        ttk.Label(self.range_frame, text='X min'
                ).grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.x_min_range = tk.StringVar()
        self.x_min_range.set('0')
        ttk.Entry(self.range_frame, textvariable=self.x_min_range, width=10,
                 justify=tk.CENTER).grid(row=2, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Y min
        ttk.Label(self.range_frame, text='Y min'
                ).grid(row=2, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.y_min_range = tk.StringVar()
        self.y_min_range.set('0')
        ttk.Entry(self.range_frame, textvariable=self.y_min_range, width=10,
                 justify=tk.CENTER).grid(row=2, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # X max
        ttk.Label(self.range_frame, text='X max'
                ).grid(row=3, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.x_max_range = tk.StringVar()
        self.x_max_range.set('100')
        ttk.Entry(self.range_frame, textvariable=self.x_max_range, width=10,
                 justify=tk.CENTER).grid(row=3, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Y max
        ttk.Label(self.range_frame, text='Y max'
                ).grid(row=3, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.y_max_range = tk.StringVar()
        self.y_max_range.set('100')
        ttk.Entry(self.range_frame, textvariable=self.y_max_range, width=10,
                 justify=tk.CENTER).grid(row=3, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )

        # LEGEND PANEL
        self.legend_frame = ttk.LabelFrame(self.plot_tab, text='Legend position')
        self.legend_frame.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                               padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                              )
        temp = "'Best' lets matplotlib decide the position."
        ttk.Label(self.legend_frame, text=temp
                ).grid(row=0, column=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        # Legend position
        self.legend = tk.IntVar()
        self.legend.set(4)
        ttk.Radiobutton(self.legend_frame, text='Upper left', variable=self.legend, value=0
                      ).grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )
        ttk.Radiobutton(self.legend_frame, text='Upper right', variable=self.legend, value=1
                      ).grid(row=1, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )
        ttk.Radiobutton(self.legend_frame, text='Lower left', variable=self.legend, value=2
                      ).grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )
        ttk.Radiobutton(self.legend_frame, text='Lower right', variable=self.legend, value=3
                      ).grid(row=2, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )
        ttk.Radiobutton(self.legend_frame, text='Best', variable=self.legend, value=4
                      ).grid(row=1, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY)
        self.legend_var ={'0': 'upper left',
                          '1': 'upper right',
                          '2': 'lower left',
                          '3': 'lower right',
                          '4': 'best'
                         }

        # CUSTOMIZE PANEL
        self.custom_frame = ttk.LabelFrame(self.plot_tab, text='Customize')
        self.custom_frame.grid(row=3, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                               padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                              )
        self.grid_state = tk.IntVar()
        self.grid_state.set(1)
        ttk.Checkbutton(self.custom_frame, text='Show grid', variable=self.grid_state
                      ).grid(row=0, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )
        # APPLY BUTTON
        ttk.Button(self.plot_tab, text='Apply all', command=self.plot_curves
                 ).grid(row=4, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                        padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                       )

        # Add this tab to the notebook.
        self.tool_notebook.add(self.plot_tab, text='Plot area')

    def annotation_tab(self):
        """ Third tab managing annotations."""
        # Create annotation tab
        self.annot_tab = ttk.Frame(self.tool_notebook)

        # Comment
        ttk.Label(self.annot_tab, text='X and Y positions refer to data coordinate system.',
                 justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W+tk.N+tk.S,
                                       padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                                      )

        # TEXT PANEL
        self.text_frame = ttk.LabelFrame(self.annot_tab, text='Annotation')
        self.text_frame.grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                             padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                            )
        # Text
        ttk.Label(self.text_frame, text='Text'
                ).grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.annotation = tk.StringVar()
        self.annotation.set('Annotation_text')
        ttk.Entry(self.text_frame, textvariable=self.annotation, width=32,
                 justify=tk.CENTER).grid(row=0, column=1, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # X position of annotation
        ttk.Label(self.text_frame, text='X position'
                ).grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.annotation_x = tk.StringVar()
        self.annotation_x.set('0')
        ttk.Entry(self.text_frame, textvariable=self.annotation_x, width=10,
                 justify=tk.CENTER).grid(row=1, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Y position of annotation
        ttk.Label(self.text_frame, text='Y position'
                ).grid(row=1, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.annotation_y = tk.StringVar()
        self.annotation_y.set('0')
        ttk.Entry(self.text_frame, textvariable=self.annotation_y, width=10,
                 justify=tk.CENTER).grid(row=1, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Color
        ttk.Label(self.text_frame, text='Text color'
                ).grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.annot_color_combo = ttk.Combobox(self.text_frame,
                                              values=my_colors_white,
                                              justify=tk.CENTER,
                                              width=10
                                             )
        self.annot_color_combo.set(my_colors_white[0])
        self.annot_color_combo.grid(row=2, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                    padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                   )
        # Binding the callback to self.arrow_color_combo is not necessary si 'apply all' will get the color value.
        # Font size
        ttk.Label(self.text_frame, text='Font size'
                ).grid(row=2, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.annot_size = tk.StringVar()
        self.annot_size.set('10')
        ttk.Entry(self.text_frame, textvariable=self.annot_size, width=10,
                 justify=tk.CENTER).grid(row=2, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Show annotation
        self.annot_state = tk.IntVar()
        self.annot_state.set(0)
        # No callback since 'Apply all' redraw the plot with or without the annotation.
        ttk.Checkbutton(self.text_frame, text='Show the annotation', variable=self.annot_state
                       ).grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.N+tk.S,
                                           padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                          )

        # ARROW PANEL
        self.arrow_frame = ttk.LabelFrame(self.annot_tab, text='Arrow properties')
        self.arrow_frame.grid(row=3, column=0,  columnspan=2,sticky=tk.E+tk.W+tk.N+tk.S,
                              padx=self.CONTAINER_PADX, pady=self.CONTAINER_PADY
                             )
        # X position of arrow head
        ttk.Label(self.arrow_frame, text='Head X pos.'
                ).grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.arrow_head_x = tk.StringVar()
        self.arrow_head_x.set('0')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_x, width=10,
                 justify=tk.CENTER).grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Y position of arrow head
        ttk.Label(self.arrow_frame, text='Head Y pos.'
                ).grid(row=0, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.arrow_head_y = tk.StringVar()
        self.arrow_head_y.set('0')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_y, width=10,
                 justify=tk.CENTER).grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Length of arrow head
        ttk.Label(self.arrow_frame, text='Head length'
                ).grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.arrow_head_length = tk.StringVar()
        self.arrow_head_length.set('10')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_length, width=10,
                 justify=tk.CENTER).grid(row=1, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Width of arrow head
        ttk.Label(self.arrow_frame, text='Head width'
                ).grid(row=1, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.arrow_head_width = tk.StringVar()
        self.arrow_head_width.set('4')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_head_width, width=10,
                 justify=tk.CENTER).grid(row=1, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Color of arrow
        ttk.Label(self.arrow_frame, text='Line color').grid(row=2,
                        column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.E+tk.W+tk.N+tk.S)
        self.arrow_color_combo = ttk.Combobox(self.arrow_frame,
                                                values=my_colors_white,
                                                justify=tk.CENTER,
                                                width=10
                                                )
        self.arrow_color_combo.set(my_colors_white[0])
        self.arrow_color_combo.grid(row=2, column=1, sticky=tk.E+tk.W+tk.N+tk.S,
                                    padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                   )
        # Binding the callback to self.arrow_color_combo is not necessary si 'apply all' will get the color value.
        # Width of arrow
        ttk.Label(self.arrow_frame, text='Line width'
                ).grid(row=2, column=2, sticky=tk.E+tk.W+tk.N+tk.S,
                       padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                      )
        self.arrow_width = tk.StringVar()
        self.arrow_width.set('0.5')
        ttk.Entry(self.arrow_frame, textvariable=self.arrow_width, width=10,
                 justify=tk.CENTER).grid(row=2, column=3, sticky=tk.E+tk.W+tk.N+tk.S,
                                         padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                                        )
        # Show arrow.
        self.arrow_state = tk.IntVar()
        self.arrow_state.set(0)
        # No callback since 'Apply all' redraw the plot with or without the annotation.
        ttk.Checkbutton(self.arrow_frame, variable=self.arrow_state,
                        text='Show the arrow connected to the annotation'
                       ).grid(row=5, column=0, columnspan=4, sticky=tk.W+tk.N+tk.S,
                             padx=self.WIDGET_PADX, pady=self.WIDGET_PADY
                            )

        # APPLY BUTTON
        ttk.Button(self.annot_tab, text='Apply all',
                  command=self.plot_curves, width=6).grid(
                  row=4, column=0, padx=self.WIDGET_PADX, pady=self.WIDGET_PADY, sticky=tk.E+tk.W+tk.N+tk.S)

        # Add this tab to the notebook.
        self.tool_notebook.add(self.annot_tab, text='Annotation')


if __name__ == '__main__':
    app = Application()
    # Launch the GUI mainloop which should always be the last instruction!
    app.mainloop()