# PlotView
PlotView is a **curve plotter** using CSV files containing each 1 curve (X and Y coordinates for each curve point). The CSV file will be prepared using pandas library into a strict CSV format (delimiter is comma). The first row should contain the type of value for X and Y and possibly the units.
The appearance of curves and axis scales should be customized in PlotView. 

It is my first program written in Python so I learn while I code. 

Check the Wiki/To Do page for future steps.

## My goals
- Application to learn the basics of Python.
- Hopefully make a tool which will be useable to plot test data at work.

## Useful informations
It is programmed in python3 using the following modules : Tkinter, Pandas, Matplotlib. Matplotlib Figure and Navigation Tool Bar will be embedded in Tkinter GUI since it is not possible to update the Matplotlib window in an interactive way.

The GUI will be make with **Tkinter** (and maybe tkinter.ttk later on) due to:
- *portability* to Linux & Windows
- *ease of programming* for a beginner

matplotlib will be used to handle the plotting part. The Figure will be embedded in tkinter window.

### test/
This folder will contain my test curves and on-going stuff.
