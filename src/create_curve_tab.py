try:
    #from collections import OrderedDict
    #import configparser
    import tkinter as tk
    from tkinter import font
    #from tkinter import messagebox as msg
    #from tkinter import filedialog
    import tkinter.ttk as ttk
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')
    # TODO how to use same exception for all imports. Class? 

class CreateCurveTab():
    """GUI tabbed panel for curve creation.
    
    Constants:
        - MAX_STR_CREATE_CURVE: int -> number of caracters to be displayed to show the
                                        working directory or file name
    
    Variables:
            - work_dir: string -> directory path showing working directory.
            - work_dir_txt: string -> end of working directory to be displayed in label
            - work_file: string -> file path to CSV file.
            - work_file_txt: string -> end of file path to be displayed in label
    """

    def __init__(self, parent):
        self.parent = parent
        # Max length of string showed by 'Create curve' labels.
        # This value depends on window width, type of font and font size.
        self.MAX_STR_CREATE_CURVE = 39

        # 'work_dir_set' defines the directory for the CSV filedialog.
        self.work_dir = ''
        self.work_dir_txt = tk.StringVar(self, value=self.create_underscores())
        # Path to CSV file
        # work_file define the CSV file path
        self.work_file = ''
        self.work_file_txt = tk.StringVar(self, value=self.create_underscores())
        # Curve creation label showing the curve name
        self.curve_label = tk.StringVar(self, value='No CSV files selected.')

    def create_underscores(self):
        """ Creates a string with underscores to fill the 'work_dir' and 'work file' labels when empty.

            Empty label and filled label are both limited to 'MAX_STR_CREATE_CURVE' characters.
            This way, the label layout is visually more consistent.
        """
        underscores = list()
        for i in range(0, self.MAX_STR_CREATE_CURVE):
            underscores.append('_')
        return ''.join(underscores)
