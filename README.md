# PlotView
PlotView is a curve plotter - only simple curves defined by a CSV file defining X and Y coordinates for points.
It is my first program written in python.

## My goals
- Application to learn the basics of python
- Hopefully make a tool which will be useable to plot test data.


## Data organization
- 'Curve' object:
  - Attributes:
     - id -> integer
     - name -> string
     - x_type (temps) -> string
     - y_type (value) -> string
     - number_points -> integer
     - point_array -> table of floats 2*number_points see numpy to handle the array
     - visibility -> boolean
     - line_color -> string (list of colors at beginning and RGB after ?)
     - line_width -> float (define a range)
     - line_style -> string (define a list of possible types)
     - line_marker -> string (define a list of possible types)
     - line_marker_size -> float (define a range)
  - Methods
     - read_data -> read the file and stores in point_array
     - plot_curve -> plot the curve with matplotlib
     - show_curve -> activated by a check boX
     - hide_curve -> activated by the same check box
     - get_curve_prop -> get the curve properties given by user through GUI
     - set_curve_prop -> set the curve properties on the plot

- Global variables
  - plot_title -> string (can be empty)
  - plot_x_label -> string (can be empty)
  - plot_y_label -> string (can be empty)
  - x_range_min -> float
  - x_range_max -> float
  - y_range_min -> float
  - y_range_max -> float
  - range_toggle -> float (radio button defining if user range is used or if autoscale is used
  - legend_position -> integer (1 to 4 defining the corner position in the plot)
  - grid_toggle -> boolean (grid visibility on/off)
  - dark_toggle -> boolean to switch the theme black/white
    - bg_color -> string (color of background: black/white)
    - title_color -> string (color of background: black/white)
    - axis_color -> string (color of background: black/white)
    - grid_color -> string (color of background: black/white)
    - legend_color -> string (color of background: black/white)

Algorithm
=========
Development steps
-----------------
Step 1
    Without GUI
    Read 2 data files (csv)
    Store the data in the 'Curve' attributes
    Plot the 2 curves with matplotlib

Step 2
    Without GUI
    Manage the curves visibility: on/off
    Manage the line properties

Step 3
    With GUI
    Read 2 data files (csv)
    Store the data in the 'Curve' attributes
    Plot the 2 curves with matplotlib

Step 4
    With GUI
    Manage the curves visibility: on/off
    Manage the line properties

Step 5
    With GUI
    Export image of plot in different formats
