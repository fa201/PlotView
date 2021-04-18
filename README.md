# PlotView
PlotView plots curves from CSV data file. The appearance of curves (color, line width, etc.) can be customized and one annotation can also be added if you need to highlight a point of interest.
My goals are:
* Application to learn the basics of Python and simple GUI programming.
* Hopefully make a tool which will be useable to plot test data at work.

![PlotView_example](./image/PlotView_example_1.png)

# Useful informations
The GUI will be make with **Tkinter** due to:
* *portability* to Linux & Windows
* *ease of programming* for a beginner
Matplotlib Figure and Navigation Tool Bar will be embedded in tkinter GUI since it is not possible to update the matplotlib window in an interactive way.

## Expected CSV format
**Each file contain 1 curve** (X and Y coordinates for each point of the curve). The CSV file will be prepared beforehand, using pandas for example, to produce a **strict CSV format with a comma as delimiter between both columns**. The first row should contain the type of value for X and Y.

## Folders
* 'help' gathers HTML help files launched through the *help* menu.
* 'image' contains a few pictures of plot examples.
* 'test' contains a few test curves.

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
* one annotation can be created.

Enjoy !
