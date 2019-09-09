# -*- coding: utf8 -*-
# Plot View program
# Class Curve definition

import sys

class Curve:
    """Contains all the data relative to a curve including its appearance."""

    def __init__(self, curve_id, name):
        self.curve_id = curve_id
        self.curve_name = name  # name of curve given by user and shown on PV GUI
        self.curve_x_type = ''  # x type of data and y type of data as read in the curve file
        self.curve_y_type = ''
        self.curve_number_points = 0  # number of points in the curve as read in the curve file
        # TODO                        # array of X and Y coordinates for plot
        self.curve_visibility = False  # visibility of curve in the plot
        self.curve_line_color = "black"  # line color of curve -> string
        self.curve_line_width = 1.0  # line width of curve -> float
        self.curve_line_width = "solid"  # line style of curve -> string
        self.curve_line_marker = "circle"  # line marker (symbol) of curve -> string
        self.curve_line_marker_size = 1.0  # line marker size (size of symbol) of curve -> float

    def set_curve_type(self, curve_id, x_type, y_type):
        """Set the x type of data and y type of data as read in the curve file """
        self.curve_x_type = x_type
        self.curve_y_type = y_type

    def get_curve_x_type(self):
        """Get the x type of data as read in the curve file """
        return self.curve_x_type

    def get_curve_y_type(self):
        """Get the y type of data as read in the curve file """
        return self.curve_y_type

# Test for Curve object
curve_a = Curve(10, 'curve_named_toto')
print("Curve id: {0}".format(curve_a.curve_id))
print("Curve name: {0}".format(curve_a.curve_name))
curve_a.set_curve_type(10, 'time', 'position')
print("Curve x type: {0}".format(curve_a.get_curve_x_type()))
print("Curve y type: {0}".format(curve_a.get_curve_y_type()))

# Normal termination and free the stack.
sys.exit(0)
