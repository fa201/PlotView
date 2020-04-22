# PlotView
PlotView is a **curve plotter** for CSV files. Each CSV fils contains 1 curve (X and Y coordinates for each curve point). The CSV file **will be prepared beforehand using pandas library into a strict CSV format** (delimiter is comma). The first row should contain the type of value for X and Y and possibly the units.
The appearance of curves and axis scales should be customized in PlotView. 

It is my first program written in *Python* so I learn while I code. 

The *Wiki* now contains some links to potential useful stuff for me (help pages or examples of codes).
The *Project* is my *To do list*.

## My goals
- Application to learn the basics of *Python.
- Hopefully make a tool which will be useable to plot test data at work.

## Useful informations
It is programmed in python3 using the following modules : *Tkinter*, *Pandas*, *Matplotlib*.
*Matplotlib Figure* and *Navigation Tool Bar* will be embedded in *Tkinter* GUI beacause it is not possible to update the *Matplotlib* window in an interactive way.

The GUI will be make with *Tkinter* (and maybe tkinter.ttk later on) due to:
- **portability** to Linux & Windows
- **ease of programming** for a beginner

*Matplotlib* will be used to handle the plotting part. The *Figure* will be embedded in a *tkinter* window.

Currently, there is no help, but there will we some help and advice. Yet the aim of the GUI is to be quite self-explanatory for most part.

### test/
This folder will contain my test curves that you can use.
