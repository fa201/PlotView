# -*- coding: utf8 -*-
# Plot View program
# GUI with tkinter
# Voir https://python-django.dev/page-python-modules-package-module-cours-debutants-informatique-programmation pour découper les scripts

import tkinter as tk
import tkinter.messagebox
import sys
import webbrowser

# Root window
root = tk.Tk()
root.title('PlotView v0')
root.geometry('800x600+0+0')  # Size an location of root window

# Callbacks
def quit_root():  # Quits mainloop
    root.quit()

def dialog_about_help():  # Shows the dialog for the Help/About menu
    dial = tkinter.messagebox.showinfo('About', 
    'PlotView source code is available at https://github.com/fa201/PlotView/.')

def dialog_licence_help():  # Opens the licence page of Github repo from the Help/Licence menu
    webbrowser.open_new_tab(
    'https://github.com/fa201/PlotView/blob/master/LICENSE')

# ------------------------------------------------------------------------------
# Menus for root window
# ---------------------
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
menu_file.add_command(label='Export image')
menu_file.add_command(label='Quit', command=quit_root)

# Preferences Menu
menu_pref.add_command(label='Type of export image')

# Help Menu
menu_help.add_command(label='Help on PlotView')
menu_help.add_command(label='Licence GPLv3', command=dialog_licence_help)
menu_help.add_command(label='About', command=dialog_about_help)

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# GUI main layout
# ---------------------
# Graph title area with 3 Entries
frame_title = tk.LabelFrame(root, text='Titles for graph', labelanchor='n')
frame_title.grid(row=0, column=0, padx=5, pady=5, stick='nesw')
tk.Label(frame_title, text='Global title').grid(row=0, column=0, padx=5, pady=0, stick='e')
tk.Entry(frame_title, width=20).grid(row=0, column=1, padx=5, pady=0, stick='w')  # TODO: add textvariable=.....
tk.Label(frame_title, text='Title for X axis').grid(row=1, column=0, padx=5, pady=0, stick='e')
tk.Entry(frame_title, width=20).grid(row=1, column=1, padx=5, pady=0, stick='w')  # TODO: add textvariable=.....

tk.Label(frame_title, text='Title for Y axis').grid(row=2, column=0, padx=5, pady=0, stick='e')
tk.Entry(frame_title, width=20).grid(row=2, column=1, padx=5, pady=0, stick='w')  # TODO:add textvariable=.....

# TODO: créer des variables pour les padx et pady pour chaque frame ?

# Plot ranges for X and Y 
radio_plot_scale_var = tk.IntVar()  # Variable for radio set to 1
radio_plot_scale_var.set(1)
frame_plot_range = tk.LabelFrame(root, text='Plot ranges for X and Y axis', labelanchor='n')
frame_plot_range.grid(row=0, column=1, padx=5, pady=5, stick='nesw')

# Frame created to gather and lay the radio buttons out
frame_radio_plot_range = tk.Frame(frame_plot_range) 
frame_radio_plot_range.grid(row=0, column=0, padx=0, pady=0, columnspan=4, sticky='w')

tk.Radiobutton(frame_radio_plot_range, text='Autoscale', variable=radio_plot_scale_var, value=1).grid(row=0, column=0, stick='w')
tk.Radiobutton(frame_radio_plot_range, text='User defined', variable=radio_plot_scale_var, value=2).grid(row=0, column=1, stick='w')

tk.Label(frame_plot_range, text='User defined ranges:').grid(row=1, column=0, padx=5, pady=0, columnspan=4, stick='w')

tk.Label(frame_plot_range, text='X min').grid(row=2, column=0, padx=5, pady=0)
tk.Entry(frame_plot_range, width=5).grid(row=2, column=1, padx=5, pady=0)  # TODO: add textvariable=.....


tk.Label(frame_plot_range, text='X max').grid(row=2, column=2, padx=5, pady=0)
tk.Entry(frame_plot_range, width=5).grid(row=2, column=3, padx=5, pady=0)  # TODO: add textvariable=.....

tk.Label(frame_plot_range, text='Y min').grid(row=3, column=0, padx=5, pady=0)
tk.Entry(frame_plot_range, width=5).grid(row=3, column=1, padx=5, pady=0)  # TODO: add textvariable=.....

tk.Label(frame_plot_range, text='Y max').grid(row=3, column=2, padx=5, pady=0)
tk.Entry(frame_plot_range, width=5).grid(row=3, column=3, padx=5, pady=0)  # TODO: add textvariable=.....

# Frame plot customization
frame_plot_custo = tk.LabelFrame(root, text='Plot customization', labelanchor='n')
frame_plot_custo.grid(row=0, column=2, padx=5, pady=5, stick='nesw')
radio_plot_custo_legend = tk.IntVar()  # Variable for radio set to 1
radio_plot_custo_legend.set(1)

tk.Label(frame_plot_custo, text='Position of legend in the plot:').grid(row=0, column=0, padx=0, pady=0)
# Frame created to gather and lay the radio buttons out
frame_plot_legend = tk.Frame(frame_plot_custo) 
frame_plot_legend.grid(row=0, column=0, padx=0, pady=0)

tk.Radiobutton(frame_plot_legend, text='Lower right', variable=radio_plot_custo_legend, value=1).grid(row=1, column=1, stick='w')
tk.Radiobutton(frame_plot_legend, text='Upper right', variable=radio_plot_custo_legend, value=2).grid(row=0, column=1, stick='w')
tk.Radiobutton(frame_plot_legend, text='Upper left', variable=radio_plot_custo_legend, value=3).grid(row=0, column=0, stick='w')
tk.Radiobutton(frame_plot_legend, text='Lower left', variable=radio_plot_custo_legend, value=4).grid(row=1, column=0, stick='w')

# Frame created to gather and lay the checkbuttons out
frame_plot_other = tk.Frame(frame_plot_custo)
frame_plot_other.grid(row=1, column=0, padx=0, pady=0)

check_display_grid_var = tk.IntVar()
tk.Checkbutton(frame_plot_other, text='Grid', variable=check_display_grid_var).grid(row=0, column=0, padx=0, pady=0)

check_display_dark_var = tk.IntVar()
tk.Checkbutton(frame_plot_other, text='Dark background', variable=check_display_dark_var).grid(row=0, column=1, padx=0, pady=0)


# Curve management 
frame_curve_management = tk.LabelFrame(root, text='Curve management', labelanchor='n')
frame_curve_management.grid(row=1, column=0, padx=5, pady=5, stick='nesw', columnspan=3)

# Labels for all the curve widgets
tk.Label(frame_curve_management, text='Curve #').grid(row=0, column=0, padx=0, pady=0)
tk.Label(frame_curve_management, text='Curve name').grid(row=0, column=1, padx=0, pady=0)
tk.Label(frame_curve_management, text='Show').grid(row=0, column=2, padx=0, pady=0)
tk.Label(frame_curve_management, text='Color').grid(row=0, column=3, padx=0, pady=0)
tk.Label(frame_curve_management, text='Line width').grid(row=0, column=4, padx=0, pady=0)
tk.Label(frame_curve_management, text='Line style').grid(row=0, column=5, padx=0, pady=0)
tk.Label(frame_curve_management, text='Marker type').grid(row=0, column=6, padx=0, pady=0)

# Plot button
tk.Button(frame_curve_management, text='Plot the\n selected\n curves').grid(row=0, column=7, rowspan=2)

# Curve 1 widgets. This block will be repeated several times for each line of widget
tk.Label(frame_curve_management, text='1').grid(row=1, column=0, padx=2, pady=0)
tk.Entry(frame_curve_management, width=20).grid(row=1, column=1, padx=2, pady=0, stick='w')  # TODO: add textvariable=entry_curve1_name ?
check_display_curve1_var = tk.IntVar()
tk.Checkbutton(frame_curve_management, variable=check_display_curve1_var).grid(row=1, column=2, padx=2, pady=0)


# ------------------------------------------------------------------------------


# Quit actions
root.protocol('WM_DELETE_WINDOW', quit_root)  # Allows root window to be closed by the closing icon
root.mainloop()  # Event loop
root.destroy()  # Destroy the root window
