# -*- coding: utf-8 -*-

"""PlotView read a data file plot the data curve using matplotlib.
	
TODO: Additional explanation
    Variables are created next to the place where they are used
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import webbrowser


# ====================  Class  ===================================
class Curve:
    """Contains all the data relative to a curve:
        - curve ID and name
        - CSV file path
        - dataframe for (X,Y) points
        - curve line appearance (color, width, etc.)
    """

    count = 1  # Count the number of curves created

    def __init__(self, name, file):
        self.c_id = str(Curve.count)  # Curve ID: must be unique. Formatted to string to avoid this later on.
        self.c_name = name  # Curve name entered by user in PV GUI 
        self.c_file = file  # Path of data file given by user in PV GUI
        self.c_data = self.read_file(file)  # X, Y dataframe defining the curve from file
        self.c_data_type = self.read_data_type(file)  # Dictionnary: 'x_type', 'y_type'
        self.c_visibility = False  # GUI indicator to show the curve in the plot
        self.c_color = 'black'  # Line color of curve -> string
        self.c_width = 1.0  # line width of curve -> float TODO: what are the limits?
        self.c_style = 'solid'  # line style of curve -> string TODO: what are the options?
        self.c_marker = 'o'  # line marker (symbol) of curve -> string TODO: what are the options?
        self.c_marker_size = 1.0  # line marker size (size of symbol) of curve -> float TODO: what are the limits?
        Curve.count += 1

    def read_file(self, file):
        """Read the curve file (only 2 columns) as the file is processed out of PlotView:
                - delete unused data and headers: only 1 line for header
                - rename column headers if necessary
                - strip unwanted spaces
                - make sure that comma is the delimiter
        """
        df = pd.read_csv(file, delimiter=',', header=0, dtype=float)  # header index=0 to skip string content. float converts data into float (necessary in order to plot)
        print('Imported CSV file: ', file)
        print('Size of data (lines, colums):', df.shape)  # TODO: this should appear on status bar along with the file pat and name
        print(df.dtypes) # To confirm that the data type is float
        return df

    def read_data_type(self, file):
        """Read only the header line to set c_data_type list (X type of data, Y type of data)"""
        df = pd.read_csv(file, delimiter=',', header=None, nrows=1)  # Read only data types
        d = {}
        d.update({'x_type': df.iloc[0, 0], 'y_type': df.iloc[0, 1]})
        return d

    def plot_df(self, axes):
        """Plot the curve with all relevant Curve properties"""
        plt.plot(self.c_data.iloc[:, 0], self.c_data.iloc[:, 1],
                label=self.c_name, c=self.c_color, lw=self.c_width,
                ls=self.c_style, marker=self.c_marker,
                markersize=self.c_marker_size)
# ====================================================================


# ====================  Variables  ===================================
# Root window
root = tk.Tk()
root.title('PlotView v0.2')
#root.geometry(str(root.winfo_screenwidth()) + 'x' + str(root.winfo_screenheight()) + '+0+0')  # Set the size to max but it lloks like it is too big on Ubuntu. TODO: test on Windows
root.geometry('1366x768+0+0')
# ====================================================================


# ====================  Callbacks  ===================================
# Quits mainloop
def quit_root():
    root.quit()

# Shows the dialog from the Help/About menu
def dialog_about_help():
    dial = tkinter.messagebox.showinfo('About',
    'PlotView source code is available at https://github.com/fa201/PlotView/.')

# Opens the licence page of Github repo from the Help/Licence menu
def dialog_licence_help():
    webbrowser.open_new_tab(
    'https://github.com/fa201/PlotView/blob/master/LICENSE')
# ====================================================================


# ====================  Menus  ===================================
# Main menu 
menu_main = tk.Menu(root)
menu_file = tk.Menu(menu_main, tearoff='False')  # Disables tear off menu
menu_pref = tk.Menu(menu_main, tearoff='False')
menu_help = tk.Menu(menu_main, tearoff='False')

menu_main.add_cascade(label='File', menu=menu_file)  # Adds menu_file in menu_main
menu_main.add_cascade(label='Preferences', menu=menu_pref)
menu_main.add_cascade(label='Help', menu=menu_help)

root.config(menu=menu_main)  # Link of main menu to root window

# File Menu
menu_file.add_command(label='Load session', state='disabled')  # TODO: activate XML session loading
menu_file.add_command(label='Save session as', state='disabled')  # TODO: activate XML session exporting
menu_file.add_command(label='Export image', state='disabled')
menu_file.add_command(label='Quit', command=quit_root)

# Preferences Menu
menu_pref.add_command(label='Type of export image', state='disabled')

# Help Menu
menu_help.add_command(label='Help on PlotView', state='disabled')
menu_help.add_command(label='Licence GPLv3', command=dialog_licence_help)
menu_help.add_command(label='About', command=dialog_about_help)
# ====================================================================


# ====================  Matplotlib embedded   ===================================





# ====================================================================


# ====================  Main program  ===================================
# Curve list to manage the plots
curves = []

# Test of features - TO BE REMOVED LATER
c1 = Curve('curve 1', 'test/curve1.csv')
curves.append(c1.c_name)
c2 = Curve('curve 2', 'test/curve2.csv')
curves.append(c2.c_name)
print('List des éléments de \"curves\" : ', curves)
#

# Plot creation TODO: needs explanations (why it works) and rework
fig, ax = plt.subplots(1)
c1.plot_df(ax)
plt.draw()
plt.pause(1)
c2.plot_df(ax)
plt.draw()
plt.show()

# Quit actions
root.protocol('WM_DELETE_WINDOW', quit_root)  # Allows root window to be closed by the closing icon
root.mainloop()  # Event loop
root.destroy()  # Destroy the root window

# Normal termination and free the stack.
sys.exit(0)
