# PlotView
PlotView is a **curve plotter** using CSV files. Each file contain 1 curve (X and Y coordinates for each point of the curve). The CSV file will be prepared beforehand, using pandas for example, to produce a strict CSV format with a comma as delimiter between both columns. The first row should contain the type of value for X and Y.
The appearance of curves and axis scales can be customized in PlotView.
![PlotView_example](./image/PlotView_example.png)

## My goals
* Application to learn the basics of Python and simple GUI programming.
* Hopefully make a tool which will be useable to plot test data at work.

## Useful informations
It is programmed in python3 using the following modules : tkinter, pandas, matplotlib. Matplotlib Figure and Navigation Tool Bar will be embedded in tkinter GUI since it is not possible to update the matplotlib window in an interactive way.

The GUI will be make with **Tkinter** due to:
* *portability* to Linux & Windows
* *ease of programming* for a beginner

### test/
This folder contains a few test curves.

### help/
This folder contains HTML help files launched through the *help* menu.

# Required Python packages.
PlotView needs the following packages to run.
* Python 3
* pandas 1.0.1
* matplotlib 3.2.0
* tkinter 8.6
Note that the above versions are those used for the development. If you have a lower version for a package, it may work. In case of trouble, please update the packages to these versions at least.

# Limitations of PlotView
* the size of the window is 1280 x 720 pixels so your screen has to be bigger than this.
* extensive tests are not yet done, so there is probably some bugs.

Enjoy !
