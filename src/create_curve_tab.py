try:
    # from collections import OrderedDict
    # import configparser
    import tkinter as tk
    from tkinter import font
    # from tkinter import messagebox as msg
    from tkinter import filedialog
    import tkinter.ttk as ttk
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')
    # TODO how to use same exception for all imports. Class?


class CreateCurveTab():
    """GUI tabbed panel for curve creation.

    Attributes:
            - work_dir: string -> directory path showing working directory.
            - work_dir_txt: string -> end of working directory to be displayed in label
            - work_file: string -> file path to CSV file.
            - work_file_txt: string -> end of file path to be displayed in label
    """

    def __init__(self, parent):
        self.parent = parent
        # Frame holds all the widgets for this tabbed panel.
        self.curve_tab = ttk.Frame(self.parent.tool_notebook)
        # Allow the column to expand for children widgets
        self.curve_tab.columnconfigure(index=0, weight=1)
        self.setup_create_curve_tab()
        self.create_curve_panel()
        # Caution: notebook is in Application

    def setup_create_curve_tab(self):
        """Set up parameters for this tabbed panel

        Labels showing directory and files pathes have a somewhat constant width to look better in the GUI layout. Empty characters are replaced by '_'. 

        Attributes:
        - MAX_STR_CREATE_CURVE: int -> number of characters. Depends on window width, font and font size.
        - work_dir: string -> directory path to CSV file
        - work_dir_txt: string -> above path shortened to fit in the label. Only the end part is kept.
        - work_file: string -> file path to CSV file
        - work_file_txt: string -> above path shortened to fit in the label. Only the end part is kept.
        """
        self.MAX_STR_CREATE_CURVE = 39
        self.work_dir = ''
        self.work_dir_txt = tk.StringVar(value=self.create_underscores())
        self.work_file = ''
        self.work_file_txt = tk.StringVar(value=self.create_underscores())
        # Curve creation label showing the curve name
        self.curve_label = tk.StringVar(value='No CSV file selected.')

    def create_underscores(self):
        """ Returns a string with underscores to fill the 'work_dir' and 'work file' labels when empty.

        Empty label and filled label are both limited to 'MAX_STR_CREATE_CURVE' characters.
        This way, the label layout is visually more consistent.
        """
        underscores = list()
        for i in range(0, self.MAX_STR_CREATE_CURVE):
            underscores.append('_')
        return ''.join(underscores)

    def create_curve_panel(self):
        """Create widgets for creating the curve in the tabbed panel

        2 columns of widgets are created in a frame.

        Attributes:
        - create_curve_frame: LabelFrame -> holds all the widgets for creating curves

        """
        self.create_curve_frame = ttk.LabelFrame(
            self.curve_tab, text='Create curve')
        self.create_curve_frame.grid(row=0, column=0)
        # Allow the columns to expand for children widgets
        for i in range(0, 2):
            self.create_curve_frame.columnconfigure(index=i, weight=1)
        # Working directory widgets TODO style à définir
        # ttk.Button(self.create_curve_frame, text='Work dir.',
        #           command=self.choose_dir, style='w9.TButton').grid(row=0, column=0)
        ttk.Button(self.create_curve_frame, text='Work dir.',
                   command=self.choose_dir).grid(row=0, column=0)
        ttk.Label(self.create_curve_frame,
                  textvariable=self.work_dir_txt
                  ).grid(row=0, column=1)
        # CSV file widget
        # ttk.Button(self.create_curve_frame, text='CSV file',
        #           command=self.choose_file, style='w9.TButton'
        #           ).grid(row=1, column=0)
        ttk.Button(self.create_curve_frame, text='CSV file',
                   command=self.choose_file).grid(row=1, column=0)
        ttk.Label(self.create_curve_frame, textvariable=self.work_file_txt
                  ).grid(row=1, column=1)
        # Curve name widget
        curve_name_label = ttk.Label(
            self.create_curve_frame, text='Curve name')
        curve_name_label.grid(row=2, column=0)
        self.curve_label = tk.StringVar(value='Curve_name')
        ttk.Entry(self.create_curve_frame, textvariable=self.curve_label, width=30,
                  justify=tk.CENTER).grid(row=2, column=1)
        # Curve create widget
        # ttk.Button(self.create_curve_frame, text='Create curve',
        #           command=self.curve_create, style='w4.TButton'
        #           ).grid(row=3, column=0, columnspan=2)
        """
        ttk.Button(self.create_curve_frame, text='Create curve',
                   command=self.curve_create).grid(row=3, column=0, columnspan=2)
        """
        self.parent.tool_notebook.add(self.curve_tab, text='Curve')

    def choose_dir(self):
        """ Set the working directory to process several curves in a row.

            A file dialog allows to select the working directory path.
            Process the string of working directory to have no more than MAX_STR_CREATE_CURVE
            characters. This gives no change in layout when selecting long or short path.
            The length of string displayed should be the same as for choose_file.

            CAUTION: if the folder path is shorter than MAX_STR_CREATE_CURVE then the frame width is kept only due to curve name entry.
        """
        self.work_dir = filedialog.askdirectory(
            title='Choose a working directory for CSV files')
        # MAX_STR_CREATE_CURVE-3 to take into account the '...' prefix to the final string.
        if len(self.work_dir) > (self.MAX_STR_CREATE_CURVE-3):
            temp = ''.join(
                ['...', self.work_dir[-self.MAX_STR_CREATE_CURVE+3:]])
            self.work_dir_txt.set(temp)
            self.parent.status_bar.set_status(
                ''.join(['Working directory is set at: ', self.work_dir]))
        elif 0 < len(self.work_dir) < (self.MAX_STR_CREATE_CURVE-3):
            self.work_dir_txt.set(self.work_dir)
            self.parent.status_bar.set_status(
                ''.join(['Working directory is set at: ', self.work_dir]))
        else:
            # Dialog CANCEL returns empty string. So the initial value is reassigned to keep the layout.
            self.work_dir_txt.set(self.create_underscores())
            self.parent.status_bar.set_status(
                'WARNING - No working directory selected.')

    def choose_file(self):
        """ Get the path to the CSV file to open.

            A file dialog allows to select the file path.
            Process the string of working directory to have no more than 'MAX_STR_CREATE_CURVE'
            characters. This gives no change in layout when selecting long or short path.
            The length of string displayed should be the same as for 'choose_dir'.

            CAUTION: if the folder path is shorter than MAX_STR_CREATE_CURVE then the frame width is kept only due to curve name entry.
        """
        self.work_file = filedialog.askopenfilename(
            initialdir=self.work_dir, filetypes=[('CSV file', '*.csv')], title='Open CSV file')
        if len(self.work_file) > (self.MAX_STR_CREATE_CURVE-3):
            temp = ''.join(
                ['...', self.work_file[-self.MAX_STR_CREATE_CURVE+3:]])
            self.work_file_txt.set(temp)
            self.parent.status_bar.set_status(
                ''.join(['CSV file selected: ', self.work_file]))
        elif 0 < len(self.work_file) < (self.MAX_STR_CREATE_CURVE-3):
            self.work_file_txt.set(self.work_file)
            self.parent.status_bar.set_status(
                ''.join(['CSV file selected: ', self.work_file]))
        else:
            # Dialog CANCEL returns empty string. So the initial value is reassigned to keep the layout.
            self.work_file_txt.set(self.create_underscores())
            self.parent.status_bar.set_status(
                'WARNING - A CSV file has to be selected.')
