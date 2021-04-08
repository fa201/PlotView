# -*- coding: utf-8 -*-

""" PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    PlotView is summarized as PV in variable names.
"""


class Model:
    """ Define some default values for directories or files

        The working directory is supposed to contain several CSV curve files to plot.
        The goal is to avoid repeating navigation to the same directory for data.
        It is supposed to be changed once or a few times per PlotView session.

        The working file shows the current curve CSV file used, once the file is loaded.

        Variables:
        - work_dir: string -> complete path to the working directory
        - work_dir_txt: string -> short path showing the end of 'work_dir'
    """
    def __init__(self, application):
        self.app = application


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

    def __init__(self, path):
        # Curve ID: must be unique.
        # '0' is added from 1 to 9 to keep the order when sorted as text.
        if Curve.count < 10:
            # Format integrer to string to avoid this later on.
            self.id = '0' + str(Curve.count)
        else:
            self.id = str(Curve.count)
        # Curve ID is shown to avoid confusion until the relevant name is defined.
        self.name = 'Curve_' + self.id
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
        # TODO: what are the limits?
        self.marker_size = 1.0
        Curve.count += 1

    def read_file(self):
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
        df = pd.read_csv(self.path, delimiter=',', dtype=float)
        message = 'Curve ID {0} - size of data (lines, colums): {1}'
        # TODO: check that the status bar is updated.
        app.set_status(message.format(self.id, df.shape))
        return df
