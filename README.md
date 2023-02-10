# PlotView
PlotView plots curves from CSV data file. The appearance of curves (color, line width, etc.) can be customized. Some curves can also be hidden. One annotation can be added if you need to highlight a point of interest. PlotView can compute the 4 extrema values (Xmin, Xmax, Ymin, Ymax) for a given curve.

*ttk* is used to have a more modern look at least on Windows platorms. Note that the below picture was taken on linux Xubuntu.

My goals are:
* Application to learn the basics of Python and simple GUI programming.
* Make a tool which will be useable to plot test data at work.

![PlotView_example](./image/PlotView_example_1.png)

# Useful informations
The GUI will be make with **Tkinter** due to:
* *portability* to Linux & Windows
* *ease of programming* for a beginner

pandas and matplotlib allow to **process a lot of data points much faster than spreadsheet applications** (MS-Excel, LibreOffice Calc, etc.).

matplotlib *Figure* and *Navigation Tool Bar* will be embedded in tkinter GUI since it is not possible to update the matplotlib window in an interactive way.

## Expected CSV format
**Each file contain 1 curve** (X and Y coordinates for each point of the curve). The CSV file will be prepared beforehand, using pandas for example, to produce a **strict CSV format with a comma as delimiter between both columns**. The first row should contain the type of value for X and Y.
**tools/curve_toolbox.py** can help to prepare the CSV files.


## Folders and files
* *fresh_session.pv* is a session file which enables to clear the current data in PlotView.
* *help* folder gathers HTML help files launched through the *help* menu.
* *image* folder contains a few pictures of plot examples.
* *test* folder contains a few test curves.
* *tools* folder contains a python script *curve_toolbox.py* to help prepare the CSV files before plotting them.
* *plotview.py* is the python script.
* *session.pv* is a session file which enables to bring back the session shown on the picture: curves will be load, colors, titles and annotation are updated.

# Required Python packages.
PlotView needs the following packages to run.
* python 3
* pandas 1.0.1
* matplotlib 3.5.1 (matplotlib 3.2 gives an error)
* tkinter 8.6

Note that the above versions are those used for the development. If you have a lower version for a package, it may work. In case of trouble, please update the packages to these versions at least.

# Limitations of PlotView
* Strict CSV format with 1 curve per file.
* One annotation can be created.

Enjoy !
