# -*- coding: utf-8 -*-

try:
    from collections import OrderedDict
    # import configparser
    # import os
    import pandas as pd
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')
    # TODO how to use same exception for all imports. Class?


class Curve():
    """ Contains all the data relative to a curve.

    Class attribute 'count' is used for the curve ID 'id' and gives the number of curves created.
    'id' is the key of Curve instance dictionary.
    This key will never change whereas the user-defined 'name' can change.

    The default plotting parameters are those below (user can change them).
    Curve attributes:
        - name: string -> user-defined name. Can be changed in the PV session
        - path: string -> path to CSV file
        - input_data: dataframe -> contains (X,Y) points as read in the CSV file
        - data_type: dictionary -> contains X header and Y header
        - output_data: dataframe -> input_data with offset and scale values to be plotted
        - visibility: boolean -> flag to show the curve in the plot or not
        - color: string -> color of the curve line
        - width: float -> width of the curve line
        - style: string -> style of the curve line
        - x_offset: float -> X data offset after X data scale
        - y_offset: float -> Y data offset after Y data scale
        - x_scale: float -> X data scaling
        - y_scale: float -> Y data scaling
        TODO: add fig, ax, canvas, work_dir etc. in this docstring
    Curve methods:
        - method to read the CSV file
    """
    count = 0
    # Dictionary of curve instances.
    # Ordered dictionary is kept as the user can remind in which order the curves are created.
    dic = OrderedDict()
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
    my_linestyles = ['solid', 'dashed', 'dotted', 'dashdot']

    def __init__(self, parent, path):
        """ Create a Curve instance based on CSV file path.

            TODO: add all attributes in parameter to create a Curve when reading session file
        """
        self.parent = parent
        self.name = 'Name'
        self.path = path
        self.input_data = self.read_CSV_file(self.path)
        self.data_type = self.get_CSV_x_and_y_data_types()
        self.output_data = self.create_output_data(self.input_data)
        self.visibility = True
        self.color = Curve.my_colors[app.plot_fig_color][1]
        self.width = 1.0
        self.style = Curve.my_linestyles[0]
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

    # def read_CSV_file(self, path):
        """ Read the curve file in CSV format.

            It is necessary to convert data to float in 'read_csv' in order to plot.
            Requirements on the file format:
                - delete unused data and headers: header should be on the first line
                - rename column headers if necessary
                - only 2 columns of data (there is no error for 1 column of data but no curve is visible)
                - make sure that comma is the delimiter
                - decimal character is the point '.'
        """
        """try:
            df = pd.read_csv(self.path, delimiter=',', dtype=float)
            print('CSV file read:', self.path)
            print(df)
            return df
        except (TypeError, ValueError, IndexError, AttributeError) as e:
            msg.showerror('Error', 'The format of CSV file is not correct.\nPlease refer to files in the "test" folder.')
            Application.choose_file(app)
        # TODO: handle following exceptions: no column, more than 2 columns, strings, missing values, etc.
"""
    # def get_CSV_x_and_y_data_types(self):
        """temp = {}
        temp['x_type'] = self.input_data.columns[0]
        temp['y_type'] = self.input_data.columns[1]
        return temp

    def create_output_data(self, df):
        temp = df.copy()
        return temp
"""
    # def find_extrema(self):
        """ all values are round to 10 -> use a variable and update first label in extrema plot (number of digits)

            since pd.round() gives error on Windows, rounding is done on the float.
            The extrema values displayed on GUI are rounded but printed values are not.
        """
        """print('Extrema values for curve', self.name, 'without rounding:')

        # X min
        temp_ext_x_min = self.output_data.iloc[:, 0].min()
        self.ext_x_min = round(temp_ext_x_min, app.ROUND)
        # Find Y for X min
        temp_ext_x_min_y = self.output_data.iloc[self.output_data.iloc[:, 0].idxmin(), 1]
        self.ext_x_min_y = round(temp_ext_x_min_y, app.ROUND)
        print('X min:', temp_ext_x_min, ' @ Y:', temp_ext_x_min_y)
        app.extrema_x_min.set('X min ' + str(self.ext_x_min) + ' @ Y ' + str(self.ext_x_min_y))

        # X max
        temp_ext_x_max = self.output_data.iloc[:, 0].max()
        self.ext_x_max = round(temp_ext_x_max, app.ROUND)
        # Find Y for X max
        temp_ext_x_max_y = self.output_data.iloc[self.output_data.iloc[:, 0].idxmax(), 1]
        self.ext_x_max_y = round(temp_ext_x_max_y, app.ROUND)
        print('X max:', temp_ext_x_max, ' @ Y:', temp_ext_x_max_y)
        app.extrema_x_max.set('X max ' + str(self.ext_x_max) + ' @ Y ' + str(self.ext_x_max_y))

        # Y min
        temp_ext_y_min = self.output_data.iloc[:, 1].min()
        self.ext_y_min = round(temp_ext_y_min, app.ROUND)
        # Find X for Y min
        temp_ext_y_min_x = self.output_data.iloc[self.output_data.iloc[:, 1].idxmin(), 0]
        self.ext_y_min_x = round(temp_ext_y_min_x, app.ROUND)
        print('Y min:', temp_ext_y_min, '@ X:', temp_ext_y_min_x)
        app.extrema_y_min.set('Y min ' + str(self.ext_y_min) + ' @ X ' + str(self.ext_y_min_x))

        # Y max
        temp_ext_y_max = self.output_data.iloc[:, 1].max()
        self.ext_y_max = round(temp_ext_y_max, app.ROUND)
        # Find X for Y max
        temp_ext_y_max_x = self.output_data.iloc[self.output_data.iloc[:, 1].idxmax(), 0]
        self.ext_y_max_x = round(temp_ext_y_max_x, app.ROUND)
        print('Y max:', temp_ext_y_max, '@ X:', temp_ext_y_max_x)
        app.extrema_y_max.set('Y max ' + str(self.ext_y_max) + ' @ X ' + str(self.ext_y_max_x))
"""
