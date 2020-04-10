# PlotView
PlotView is a **curve plotter** using CSV files containing each 1 curve (X and Y coordinates for each curve point). The CSV file will be prepared using pandas library into a strict CSV format (delimiter is comma). The first 2 rows should contain:
- the type of value for X and Y
- the unit for X and Y
It is my first program written in Python so I learn while I code. 

## My goals
- Application to learn the basics of Python.
- Hopefully make a tool which will be useable to plot test data at work.

## Useful informations
It is programmed in python3 using the following modules : tkinter, pandas, matplotlib.

The GUI will be make with **Tkinter** (and maybe tkinter.ttk later on) due to:
- *portability* to Linux & Windows
- *ease of programming* for a beginner

matplotlib will be used to handle the plotting part. The Figure will be embedded in tkinter window.

### test/
This folder will contain my test and on-going stuff.
