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
root.title("PlotView v0")
root.geometry("800x600+0+0")  # Size an location of root window

# Callbacks
def quit_root():  # Quit mainloop
    root.quit()

def dialog_about_help():  # Show the dialog for the Help/About menu
    dial = tkinter.messagebox.showinfo("About", "PlotView source code is available at https://github.com/fa201/PlotView/.")

def dialog_licence_help():  # Open the licence page of Github repo from the Help/Licence menu
    webbrowser.open_new_tab('https://github.com/fa201/PlotView/blob/master/LICENSE')

# ------------------------------------------------------------------------------
# Menus for root window
# ---------------------
# Main menu
menu_main = tk.Menu(root)
menu_file = tk.Menu(menu_main, tearoff="False")  # Disables tear off menu
menu_pref = tk.Menu(menu_main, tearoff="False")
menu_help = tk.Menu(menu_main, tearoff="False")

menu_main.add_cascade(label="File", menu=menu_file)  # Adds menu_file in menu_main
menu_main.add_cascade(label="Preferences", menu=menu_pref)
menu_main.add_cascade(label="Help", menu=menu_help)

root.config(menu=menu_main)  # Link of main menu to root window

# File Menu
menu_file.add_command(label="Export image")  # Add export image command from matplotlib
menu_file.add_command(label="Quit", command=quit_root)

# Preferences Menu
menu_pref.add_command(label="Type of export image")

# Help Menu
menu_help.add_command(label="Help on PlotView")
menu_help.add_command(label="Licence GPLv3", command=dialog_licence_help)
menu_help.add_command(label="About", command=dialog_about_help)

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# GUI main layout
# ---------------------
#frame_title = LabelFrame()
#frame_plot_range = LabelFrame()
# frame_plot_custo
# frame_curve

# ------------------------------------------------------------------------------


# Quit actions
root.protocol("WM_DELETE_WINDOW", quit_root)  # Allows root window to be closed by the closing icon
root.mainloop()  # Event loop
root.destroy()  # Destroy the root window
