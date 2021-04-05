# PlotView
PlotView is a **curve plotter** using CSV files containing each 1 curve (X and Y coordinates for each curve point). The CSV file will be prepared using pandas into a strict CSV format (delimiter is comma). The first row should contain the type of value for X and Y and possibly the units.
The appearance of curves and axis scales should be customized in PlotView.

It is my first program written in Python so I learn while I code.

## My goals
* Application to learn the basics of Python.
* Hopefully make a tool which will be useable to plot test data at work.

## Useful informations
It is programmed in python3 using the following modules : tkinter, pandas, matplotlib. Matplotlib Figure and Navigation Tool Bar will be embedded in Tkinter GUI since it is not possible to update the Matplotlib window in an interactive way.

The GUI will be make with **Tkinter** due to:
* *portability* to Linux & Windows
* *ease of programming* for a beginner

matplotlib will be used to handle the plotting part. The Figure will be embedded in tkinter window.

### test/
This folder will contain my test data: CSV files.

# Limitations of PlotView
The size of the window is 1280 x 720 pixels so you screen has to be bigger than this.
