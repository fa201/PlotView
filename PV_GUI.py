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
def quit_root():  # Quit mainloop
    root.quit()

def dialog_about_help():  # Show the dialog for the Help/About menu
    dial = tkinter.messagebox.showinfo('About', 'PlotView source code is available at https://github.com/fa201/PlotView/.')

def dialog_licence_help():  # Open the licence page of Github repo from the Help/Licence menu
    webbrowser.open_new_tab('https://github.com/fa201/PlotView/blob/master/LICENSE')

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
menu_file.add_command(label='Export image')  # Add export image command from matplotlib
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
label_graph_title = tk.Label(frame_title, text='Global title')
label_graph_title.grid(row=0, column=0, padx=5, pady=0, stick='e')
entry_graph_title = tk.Entry(frame_title, width=20)  # add textvariable=.....
entry_graph_title.grid(row=0, column=1, padx=5, pady=0, stick='w')

label_graph_title_X = tk.Label(frame_title, text='Title for X axis')
label_graph_title_X.grid(row=1, column=0, padx=5, pady=0, stick='e')
entry_graph_title_X = tk.Entry(frame_title, width=20)  # add textvariable=.....
entry_graph_title_X.grid(row=1, column=1, padx=5, pady=0, stick='w')

label_graph_title_Y = tk.Label(frame_title, text='Title for Y axis')
label_graph_title_Y.grid(row=2, column=0, padx=5, pady=0, stick='e')
entry_graph_title_Y = tk.Entry(frame_title, width=20)  # add textvariable=.....
entry_graph_title_Y.grid(row=2, column=1, padx=5, pady=0, stick='w')

# Plot ranges for X and Y 
radio_plot_scale_var = tk.IntVar()
frame_plot_range = tk.LabelFrame(root, text='Plot ranges for X and Y axis', labelanchor='n')
frame_radio_plot_range = tk.Frame(frame_plot_range)  # frame created to gather and lay the radio buttons out
radio_plot_scale_var.set(1)
radio_plot_scale1 = tk.Radiobutton(frame_radio_plot_range, text='Autoscale plot', variable=radio_plot_scale_var, value=1)
radio_plot_scale2 = tk.Radiobutton(frame_radio_plot_range, text='User defined', variable=radio_plot_scale_var, value=2)
radio_plot_scale1.grid(row=0, column=0, stick='w')
radio_plot_scale2.grid(row=1, column=0, stick='w')
frame_radio_plot_range.grid(row=0, column=0, padx=0, pady=0, columnspan=4)

label_plot_user_def = tk.Label(frame_plot_range, text='User defined ranges:')
label_plot_user_def.grid(row=1, column=0, padx=5, pady=0, columnspan=4, stick='w')

label_plot_user_xmin = tk.Label(frame_plot_range, text='X min')
label_plot_user_xmin.grid(row=2, column=0, padx=5, pady=0)
entry_plot_user_xmin = tk.Entry(frame_plot_range, width=5)  # add textvariable=.....
entry_plot_user_xmin.grid(row=2, column=1, padx=5, pady=0)

label_plot_user_xmax = tk.Label(frame_plot_range, text='X max')
label_plot_user_xmax.grid(row=2, column=2, padx=5, pady=0)
entry_plot_user_xmax = tk.Entry(frame_plot_range, width=5)  # add textvariable=.....
entry_plot_user_xmax.grid(row=2, column=3, padx=5, pady=0)

label_plot_user_ymin = tk.Label(frame_plot_range, text='Y min')
label_plot_user_ymin.grid(row=3, column=0, padx=5, pady=0)
entry_plot_user_ymin = tk.Entry(frame_plot_range, width=5)  # add textvariable=.....
entry_plot_user_ymin.grid(row=3, column=1, padx=5, pady=0)

label_plot_user_ymax = tk.Label(frame_plot_range, text='Y max')
label_plot_user_ymax.grid(row=3, column=2, padx=5, pady=0)
entry_plot_user_ymax = tk.Entry(frame_plot_range, width=5)  # add textvariable=.....
entry_plot_user_ymax.grid(row=3, column=3, padx=5, pady=0)

frame_plot_custo = tk.LabelFrame(root, text='Plot customization', bg='green', labelanchor='n')

# frame_curve
frame_title.grid(row=0, column=0, padx=5, pady=5, stick='nesw')
frame_plot_range.grid(row=0, column=1, padx=5, pady=5, stick='nesw')
frame_plot_custo.grid(row=0, column=2, padx=5, pady=5, stick='nesw')



# ------------------------------------------------------------------------------


# Quit actions
root.protocol('WM_DELETE_WINDOW', quit_root)  # Allows root window to be closed by the closing icon
root.mainloop()  # Event loop
root.destroy()  # Destroy the root window
