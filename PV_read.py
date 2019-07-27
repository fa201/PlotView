# coding: utf8
# Plot View : data reader from csv file

import csv
import numpy

# Lists containing the data
curve1 = []

# Functions:
# set_plot_prop -> set the plot title, axis, scale, etc.

#class Curve(file):
    


def read_data(csv_file):
    with open(csv_file, 'r') as datafile:
        curve1 = csv.reader(datafile)
        for line in curve1:
            

