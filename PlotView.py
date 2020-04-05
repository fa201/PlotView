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

    def __init__(self, name, file):
        self.c_name = name  # Curve name entered by user in PV GUI 
        self.c_file = file  # Data file opened by user in PV GUI
        self.c_x_type = ''  # x type of data and y type of data as read in the curve file
        self.c_y_type = ''
        self.c_data = self.read_file(file)  # X, Y data defining the curve from file
        self.c_visibility = False  # GUI indicator to show the curve in the plot
        self.c_color = 'black'  # Line color of curve -> string
        self.c_width = 1.0  # line width of curve -> float TODO: what are the limits?
        self.c_style = 'solid'  # line style of curve -> string TODO: what are the options?
        self.c_marker = 'circle'  # line marker (symbol) of curve -> string TODO: what are the options?
        self.c_marker_size = 1.0  # line marker size (size of symbol) of curve -> float TODO: what are the limits?

    def read_file(self, file):
        """Read the curve file containing only 2 columns.

        The file needs to be processed before reading:
        - delete unused data and headers
        - rename column headers if necessary
        - strip unwanted spaces
        - make sure that comma is the delimiter
        """
        df = pd.read_csv(file, delimiter=',')
        print("Size of data read (lines, colums) :", df.shape)  # TODO: this should appear on status bar later
        return df
    

# Curve list to manage the plots
curves = []


#TODO : créer une liste de curve pour pouvoir en rajouter une automatiquement avec append.

# Normal termination and free the stack.
sys.exit(0)
