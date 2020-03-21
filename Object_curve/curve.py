#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test for the curve class

"""


import sys
import pandas as pd


class Curve:
    """Contains all the data relative to a curve including its appearance."""

    def __init__(self, curve_id, name, file):
		# Curve ID used to handle curves
        self.curve_id = curve_id
		# Curve name entered by user in PV GUI
        self.curve_name = name  
        # Data file opened by user in PV GUI
        self.curve_file = file
        # x type of data and y type of data as read in the curve file
        self.curve_x_type = ''  
        self.curve_y_type = ''
		# Number of points in the curve as read in the curve file
        self.curve_number_points = 0  
		# dataFrame of X and Y coordinates for plot        
        self.curve_data = DataFrame()
		# GUI indicator to show the curve in the plot                     


    def read_csv_file(self):
        """Read the curve file

        The file needs to be processed before reading:
        - clean unused data
        - rename column headers if necessary
        - strip unwanted spaces
        """

        self.curve_data = pd.read_csv(file)
        print("Taille des données (linges, colonnes) :", curve_data.shape, "\n")


# ------------------------------------------------------------------------------
# Test for Curve object. Will be removed from final script.
curve_a = Curve(10, 'curve_named_toto')
print('Curve id: {0}'.format(curve_a.curve_id))
print('Curve name: {0}'.format(curve_a.curve_name))
curve_a.set_curve_type(10, 'time', 'position')
print('Curve x type: {0}'.format(curve_a.get_curve_x_type()))
print('Curve y type: {0}'.format(curve_a.get_curve_y_type()))

# Normal termination and free the stack.
sys.exit(0)
