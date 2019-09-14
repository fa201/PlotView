#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PV_read is PlotView data reader

It reads curve data from text file (csv).
The data are then plotted.

Alternate import function: numpy.genfromtext ?
tutorial at https://www.youtube.com/watch?v=QyhqzaMiFxk&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF&index=7
https://www.youtube.com/watch?v=IbUa1tTT-7k&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF&index=8
"""

import csv
import numpy
import sys

# Lists containing the data
curve1 = []


class Curve:
    """Contains all the data relative to a curve including its appearance."""

    def __init__(self, curve_id):
        self.curve_id = curve_id


def read_data(csv_file):
    """Read the csv file and store data in a list """
    # newline='' because it is a file and not a list.
    with open(csv_file, 'r', newline='') as datafile:       
        # list() is needed to copy data to curve1.
        curve_data = list(csv.reader(datafile, delimiter=' '))  
    return curve_data

curve1 = read_data("curve1.csv")
print(curve1)

# Normal termination and free the stack.
sys.exit(0)
