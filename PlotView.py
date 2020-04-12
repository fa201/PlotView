# -*- coding: utf-8 -*-

"""PlotView read a data file plot the data curve using matplotlib.
	
Additional explanation
"""


import sys
import pandas as pd
import matplotlib.pyplot as plt


class Curve:
    """Contains all the data relative to a curve including its appearance."""

    count = 1  # Count the number of curves created

    def __init__(self, name, file):
        self.c_id = str(Curve.count)  # Curve ID: must be unique. Formatted to string to avoid this later on.
        self.c_name = name  # Curve name entered by user in PV GUI 
        self.c_file = file  # Path of data file given by user in PV GUI
        self.c_data = self.read_file(file)  # X, Y dataframe defining the curve from file
        self.c_data_type = self.read_data_type(file)  # Dictionnary: 'x_type', 'y_type'
        self.c_visibility = False  # GUI indicator to show the curve in the plot
        self.c_color = 'black'  # Line color of curve -> string
        self.c_width = 1.0  # line width of curve -> float TODO: what are the limits?
        self.c_style = 'solid'  # line style of curve -> string TODO: what are the options?
        self.c_marker = 'circle'  # line marker (symbol) of curve -> string TODO: what are the options?
        self.c_marker_size = 1.0  # line marker size (size of symbol) of curve -> float TODO: what are the limits?
        Curve.count += 1

    def read_file(self, file):
        """Read the curve file containing only 2 columns.

        The file needs to be processed before reading:
        - delete unused data and headers
        - rename column headers if necessary
        - strip unwanted spaces
        - make sure that comma is the delimiter
        """
        df = pd.read_csv(file, delimiter=',', header=0, dtype=float)  # header index=0 to skip string content. float converts data into float (necessary in order to plot)
        print(file)
        print("Size of data read (lines, colums):", df.shape)  # TODO: this should appear on status bar along with the file pat and name
        #print(df.dtypes) # To confirm that the data type is float
        print("Dataframe lu :")
        print(df)
        return df

    def read_data_type(self, file):
        df = pd.read_csv(file, delimiter=',', header=None, nrows=1)  # Read only data types
        d = {}
        d.update({'x_type': df.iloc[0, 0], 'y_type': df.iloc[0, 1]})
        return d
    
    def plot_df(self, axes):
        print('plot_df')
        #self.c_data.plot(x=self.c_data.columns[0] , y=self.c_data.iloc[:,1], ax=axes)


# Curve list to manage the plots
curves = []

# Plot creation
#fig, ax = plt.subplots(1)



###########TODO Test of features - TO BE REMOVED LATER
c1 = Curve("curve 1", "test/curve1.csv")
curves.append(c1.c_name)
#c2 = Curve("curve 2", "test/curve2.csv")
#curves.append(c2.c_name)
#print(curves)

#c1.plot_df(ax)
#plt.draw()
#plt.show()

#######################################################


# Normal termination and free the stack.
sys.exit(0)
