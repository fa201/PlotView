# -*- coding: utf-8 -*-

"""PlotView read a data file plot the data curve using matplotlib.

TODO: Additional explanation
    Variables are created next to the place where they are used
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import font
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

    def __init__(self, file):
        self.id = str(Curve.count)  # Curve ID: must be unique. Formatted to string to avoid this later on.
        self.name = 'Curve'  # Default name 
        self.file = file  # Path of data file given by user in PV GUI
        self.data = self.read_file(file)  # X, Y dataframe defining the curve from file
        self.data_type = self.read_data_type(file)  # Dictionnary: 'x_type', 'y_type'
        self.visibility = False  # GUI indicator to show the curve in the plot
        self.color = 'black'  # Line color of curve -> string
        self.width = 1.0  # line width of curve -> float TODO: what are the limits?
        self.style = 'solid'  # line style of curve -> string TODO: what are the options?
        self.marker = 'o'  # line marker (symbol) of curve -> string TODO: what are the options?
        self.marker_size = 1.0  # line marker size (size of symbol) of curve -> float TODO: what are the limits?
        Curve.count += 1

    def read_file(self, file):
        """Read the curve file (only 2 columns) as the file is processed out of PlotView:
                - delete unused data and headers: only 1 line for header
                - rename column headers if necessary
                - strip unwanted spaces
                - make sure that comma is the delimiter
        """
        # header index=0 to skip string content. Data converted into float (necessary in order to plot)
        df = pd.read_csv(file, delimiter=',', header=0, dtype=float)
        # ONLY FOR DEBUG print('Imported CSV file: ', file)
        # ONLY FOR DEBUG print()
        set_status('Curve ID {0} - size of data (lines, colums): {1}'.format(self.id, df.shape))
        return df

    def read_data_type(self, file):
        """Read only the header line to set c_data_type list (X type of data, Y type of data)"""
        df = pd.read_csv(file, delimiter=',', header=None, nrows=1)  
        d = {}
        d.update({'x_type': df.iloc[0, 0], 'y_type': df.iloc[0, 1]})
        return d

    def plot_df(self):
        """Plot the curve with all relevant Curve properties"""
        global ax
        ax.plot(self.data.iloc[:, 0], self.data.iloc[:, 1],
                label=self.name, c=self.color, lw=self.width,
                ls=self.style, marker=self.marker,
                markersize=self.marker_size)
        # Update legend
        ax.legend(loc='lower right')
        # Update the status bar with curve ID and curve name
        set_status('Curve ' + self.id + " - " + self.name + " is plotted.")
        # Updates the plot. plt.show() is not necessary to keep the plot persistent
        canvas.draw()

# ====================================================================


# ====================  Definitions  ===================================
# Constants
MAX_STR_CREATE_CURVE = 32  # Max length of string showed by 'Create curve' labels
PLOT_WIDTH = 9  # Width of Matplotlib Figure (in)
PLOT_HEIGHT = 6.68  # Height of Matplotlib Figure (in)
FONT_SIZE = 9  # Applicable for all GUI texts
CONTAINER_PADX = 7  # Padding for all containers to uniformize the look
CONTAINER_PADY = 7
WIDGET_PADX = 2  # Padding for all widgets inside a container
WIDGET_PADY = 2


# List of Curve class instances to manage the plots
curves = []

# Root window
root = tk.Tk()
root.title('PlotView v0.2')
root.geometry('1280x720+0+0')
root.resizable(0,0)  # Root window cannot be resized. 
#TODO: to be replaced by minsize() & maxsize() if I can handle properly the change of size in the GUI.

# Customized font based on TkDefaultFont
my_font = font.nametofont("TkDefaultFont")
my_font.config(size=FONT_SIZE)  # Font size reduced to have a tighter layout
# Make my_font applicable for all widgets including menus.
root.option_add("*Font", my_font)

# Working directory to look for CSV file
# work_dir defines the directory for the CSV filedialog
work_dir = '___________________________________'  
work_dir_txt = tk.StringVar()
work_dir_txt.set(work_dir)  # Displayed working dir path

# Path to CSV file
# work_file define the CSV file path
work_file = '___________________________________' 
work_file_txt = tk.StringVar()
work_file_txt.set(work_file) # Displayed working file path

# Status bar message
def set_status(string):
    """Update the status bar message."""
    status.config(text=' '+string)  # Space necessary to give more room to the left border

# ====================================================================


# ====================  Callbacks  ===================================
# === Callbacks for MENU
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

# === Callbacks for BUTTONS
def choose_dir():
    """Define the folder to search for a CSV file """
    global work_dir  # Necessary to pass the path to the opening file dialog
    directory = filedialog.askdirectory(title='Choose a working directory for CSV files')
    work_dir = directory
    # Cut the beginning of displayed string so that it fits in the layout
    # Considering the 3 dots to be added at the beginning of the cut string
    if len(work_dir) > (MAX_STR_CREATE_CURVE+3):
        temp = '...' + work_dir[-MAX_STR_CREATE_CURVE:]
        work_dir_txt.set(temp)
    else:                 
        work_dir_txt.set(work_dir)
    set_status('Working directory: {0}.'.format(work_dir))

def choose_file():
    """Define the path of CSV file to be read starting from work_dir"""
    global work_dir, work_file
    file = filedialog.askopenfilename(
                            initialdir=work_dir,
                            filetypes=[('CSV file', '*.csv')],
                            title='Open CSV file')
    work_file = file
    # Cut the beginning of displayed string so that it fits in the layout
    # Considering the 3 dots to be added at the beginning of the cut string
    if len(work_file) > (MAX_STR_CREATE_CURVE+3):
        temp = '...' + work_file[-MAX_STR_CREATE_CURVE:]
        work_file_txt.set(temp)
    else:
        work_file_txt.set(work_file)
    set_status('Selected CSV file: {0}.'.format(work_file))

def list_curve_names():
    l = []
    for i in range(len(curves)):
        l.append(curves[i].name)
    return l

def create_curve():
    """Create a Curve instance in the 'curves' list and plot it"""
    global curves
    # Creates Curve instance and adds it to the list
    curves.append(Curve(work_file))
    # Index = Curve.count-2 since:
    #   - Curve.count starts at 1
    #   - index for the 'curves' list starts at 0
    #   - Curve.count was incremented when  instance was created
    set_status('Curve {0} is created.'.format(curves[Curve.count-2].id)) 
    curves[Curve.count-2].plot_df()
    # Update curve list
    curve_name_list.set(list_curve_names())
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


# ====================  GUI  ===================================
# === Status bar at bottom of main window
status_frame = tk.Frame(root)
#status_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
status_frame.pack(expand=True, fill=tk.X, side=tk.BOTTOM)
status = tk.Label(status_frame, text=' ', bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(fill=tk.BOTH, expand=True)  # Allows the label to expand on the width
set_status('Ready.')

# === Matplotlib embedment on LH side of main window
# TODO: https://stackoverflow.com/questions/29432683/resizing-a-matplotlib-plot-in-a-tkinter-toplevel
# Plot with a defined size
fig = plt.Figure(figsize=(PLOT_WIDTH, PLOT_HEIGHT))  
ax = fig.add_subplot(111)

mat_frame = tk.Frame(root)
#mat_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
mat_frame.pack(expand=False, side=tk.LEFT)
# Creates a drawing area to put the Figure
canvas = FigureCanvasTkAgg(fig, master=mat_frame)  
canvas.draw()
# Creates the Matplotlib navigation tool bar for figures.
toolbar = NavigationToolbar2Tk(canvas, mat_frame)  
toolbar.draw()
canvas.get_tk_widget().pack()

# ==== GUI - RH tool panel  
tool_frame = tk.Frame(root)  # TODO: adjust frame width when the layout is finished
#tool_frame.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)
tool_frame.pack(expand=True, fill=tk.BOTH)
tool_notebook = ttk.Notebook(tool_frame)

# == Curve tab 
curve_tab = ttk.Frame(tool_notebook)

# = 'Create curve' panel
create_curve_frame = tk.LabelFrame(curve_tab, text='Create curve')
create_curve_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S, padx=CONTAINER_PADX, pady=CONTAINER_PADY)
# Working directory widgets
tk.Button(create_curve_frame, text='Choose directory', command=choose_dir, width=12).grid(row=0, column=0, padx=WIDGET_PADX, pady=WIDGET_PADY)
tk.Label(create_curve_frame, textvariable=work_dir_txt).grid(row=0, column=1, padx=WIDGET_PADX, pady=WIDGET_PADY) 
# CSV file widgets
tk.Button(create_curve_frame, text='Choose CSV file', command=choose_file, width=12).grid(row=1, column=0, padx=WIDGET_PADX, pady=WIDGET_PADY)  
tk.Label(create_curve_frame, textvariable=work_file_txt).grid(row=1, column=1, padx=WIDGET_PADX, pady=WIDGET_PADY)
# Create curve widget
tk.Button(create_curve_frame, text='Create', command=create_curve, width=12).grid(row=2, column=0, padx=WIDGET_PADX, pady=WIDGET_PADY)
tk.Label(create_curve_frame, text='Curve: ID - name -> {0} - Curve'.format(Curve.count)).grid(row=2, column=1, padx=WIDGET_PADX, pady=WIDGET_PADY)  # TODO: StringVar() for label (needs update after curve creation)

# = 'Select curve' panel
select_curve_frame = tk.LabelFrame(curve_tab, text='Select curve')
select_curve_frame.grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S, padx=CONTAINER_PADX, pady=CONTAINER_PADY)
tk.Label(select_curve_frame, text='Selected curve: ').grid(row=0, column=0, padx=WIDGET_PADX, pady=WIDGET_PADY)

# TODO: replace call-back affiche by real callback
def affiche(*args):
    sel = sel_curve_listbox.curselection()
    print('Valeur sélectionnée : {0}'.format(sel))
# Selection listbox with horizontal and vertical scrollbars
curve_name_list = tk.StringVar()
select_curve_y_scroll = tk.Scrollbar(select_curve_frame, orient=tk.VERTICAL)
select_curve_y_scroll.grid(row=0, column=2, sticky=tk.N+tk.S)
select_curve_x_scroll = tk.Scrollbar(select_curve_frame, orient=tk.HORIZONTAL)
select_curve_x_scroll.grid(row=1, column=1, columnspan=2, sticky=tk.E+tk.W)
sel_curve_listbox = tk.Listbox(select_curve_frame, listvariable=curve_name_list,
    xscrollcommand=select_curve_x_scroll.set,
    yscrollcommand=select_curve_y_scroll.set,
    height=5, 
    width=28)
sel_curve_listbox.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
select_curve_x_scroll['command'] = sel_curve_listbox.xview
select_curve_y_scroll['command'] = sel_curve_listbox.yview
# Binding to double left-click, Return key and num pad Return
sel_curve_listbox.bind('<Double-Button-1>', affiche)
sel_curve_listbox.bind('<Return>', affiche)
sel_curve_listbox.bind('<KP_Enter>', affiche)


#curve_name_entry = tk.Entry(create_curve_frame, width=20).grid(row=3, column=1, padx=2, pady=2)

# == Plot tab
plot_tab = ttk.Frame(tool_notebook)

# = Display the complete notebook
tool_notebook.add(curve_tab, text='Curve')
tool_notebook.add(plot_tab, text='Plot')
tool_notebook.pack(expand=False, fill=tk.BOTH)
# ====================================================================


# ====================  Main program  ===================================
# Quit actions
root.protocol('WM_DELETE_WINDOW', quit_root)  # Allows root window to be closed by the closing icon
root.mainloop()  # Event loop
root.destroy()  # Destroy the root window

# Normal termination and free the stack.
sys.exit(0)
