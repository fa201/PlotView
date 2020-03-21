#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test for the curve class

"""


import sys
import pandas as pd


class Curve:
    """Contains all the data relative to a curve including its appearance."""
    
    # Class counter to specify the next available ID for a new Curve
    next_curve_ID = 1

    def __init__(self):
		# Curve ID used to handle curves
        self.curve_id = Curve.next_curve_ID
		# Curve name entered by user in PV GUI
        self.curve_name = input("Give curve name : ")  
        # Data file opened by user in PV GUI
        self.curve_file = input("Give the name of data file : ")
        # Increment class counter for next Curve creation
        Curve.next_curve_ID +=1

# ------------------------------------------------------------------------------
# Test for Curve object. Will be removed from final script.
curve_a = Curve()
print('Curve id: {0}'.format(curve_a.curve_id))
print('Curve name: {0}'.format(curve_a.curve_name))

curve_b = Curve()
print('Curve id: {0}'.format(curve_b.curve_id))
print('Curve name: {0}'.format(curve_b.curve_name))

# Normal termination and free the stack.
#sys.exit(0)
