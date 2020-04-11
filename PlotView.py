#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PlotView read a data file plot the data curve using matplotlib.
	
Additional explanation
"""


import sys
import pandas as pd
import matplotlib.pyplot as plt


class Curve:
    """Contains all the data relative to a curve including its appearance."""

    count = 0  # Count the number of curves created

    def __init__(self, name, file):
        self.c_name = name  # Curve name entered by user in PV GUI 
        self.c_file = file  # Path of data file given by user in PV GUI
        self.c_data = self.read_file(file)  # X, Y dataframe defining the curve from file
        self.c_data_type = self.read_data_type(file)  # Dictionnary: 'x_type', 'y_type', 'x_unit', 'y_unit'
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
        df = pd.read_csv(file, delimiter=',', header=None)  # header=None to keep title and units rows
        print(file)
        print("Size of data read (lines, colums):", df.shape)  # TODO: this should appear on status bar along with the file pat and name
        return df.iloc[2:, :]  # Skip the first 2 rows (dat type and units)

    def read_data_type(self, file):
        df = pd.read_csv(file, delimiter=',', header=None, nrows=2)  # Read only data type and data units
        d = {}
        d.update({'x_type': df.iloc[0, 0], 'y_type': df.iloc[0, 1],
                'x_unit': df.iloc[1, 0], 'y_unit': df.iloc[1, 1],})
        return d
    

# Curve list to manage the plots
curves = []

###########TODO Test of features - TO BE REMOVED LATER

c1 = Curve("curve 1", "test/curve1.csv")
curves.append(c1.c_name)
c2 = Curve("curve 2", "test/curve2.csv")
curves.append(c2.c_name)
print(curves)
#print(c1.c_data)
print(c1.c_data_type)

# Normal termination and free the stack.
sys.exit(0)
