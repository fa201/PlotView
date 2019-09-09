# -*- coding: utf8 -*-
# Plot View program
# Data reader from csv file

import csv
import numpy
import sys

# Lists containing the data
global curve1
curve1 = []

# Read the data from csv file.
# Alternate import function: numpy.genfromtext ?
# tutorial at https://www.youtube.com/watch?v=QyhqzaMiFxk&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF&index=7
# https://www.youtube.com/watch?v=IbUa1tTT-7k&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF&index=8

class Curve:
    """Contains all the data relative to a curve including its appearance."""

    def __init__(self, curve_id):
        self.curve_id = curve_id


def read_data(csv_file):
    """Read the csv file and store data in a list """
    with open(csv_file, 'r', newline='') as datafile:       # newline='' because it is a file and not a list
        curve_data = list(csv.reader(datafile, delimiter=' '))  # list() is needed to copy data to curve1
    return curve_data

curve1 = read_data("curve1.csv")
print(curve1)

# Normal termination and free the stack.
sys.exit(0)
