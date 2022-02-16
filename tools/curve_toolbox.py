# -*- coding: utf-8 -*-

""" curve_toolbox is a command line set of tools to process CSV files before plot them with PlotView.


    Code hosted at: https://github.com/fa201/PlotView
    Licence: GN GPL-3.0
"""


try:
    import pandas as pd
    import glob
    import os
    from collections import defaultdict
except ModuleNotFoundError as e:
    print('The necessary Python packages are not installed.\n' + str(e))
    print('Please check the required packages at https://github.com/fa201/PlotView.')

# Move to the working directory for reading and writing CSV
os.chdir('CSV_files')


def clear_console():
    """Clear the console to display menus

        https://www.geeksforgeeks.org/clear-screen-python/
        Detect if OS is windows or Linux
    """
    # Windows clear command
    if os.name == 'nt':
        _ = os.system('cls')
    # Linux and macOS clear command
    else:
        _ = os.system('clear')

def show_title():
    """Print application title and line below"""
    title = 'Curve_toolbox: prepare CSV curves for plotting with PlotView'
    # Generate a line of '*' with the same width as the title
    print('*' * len(title))
    print(title)
    print('*' * len(title))

def show_main_menu():
    """Display main menu commands"""
    pass


def list_files():
    """List all CSV files for the user to see which files will be processed

        CSV files must be in 'CSV_files' folder
        Files will be selected in the menu through keys of file_dic

    """
    # List all CSV files in working directory
    temp_list_files = glob.glob('*.csv')
    #print('\nList of CSV files in the folder "CSV_files":\n', temp_list_files)
    file_dic = {}
    for name in temp_list_files:
        index = temp_list_files.index(name)  # Get index of current list item
        file_dic[index] = name
    #print(file_dic)

    print('CSV files found in "CSV_files" folder:')
    for key in file_dic:
        print('   ', key, '->', file_dic[key])


clear_console()
show_title()
#list_files()
show_main_menu()




"""
Convert data file to CSV format [C]
    Choose data file [D]
    Choose the delimiter between columns [SPACE], [COMMA] or [TAB]
    Choose file format [UTF] for UTF-8, [EU] for ISO.... [ANSI] for US
    Enter le line number for title of X and Y data
    Enter the number of line to be skipped before the title. [0] for none.
    Export en file_pv.csv.
    Lister les fichiers
    Back [back]
Split a CSV file into several CSV files [S] -> uniquement pour les fichiers partageant le même X
    Export en file_1.csv
    Lister les fichiers
Trim the beginning of the curve [B]
    Export en file_beg.csv
    Lister les fichiers
Trim the end of the curve [E]
    Export en file_end.csv
    Lister les fichiers
Exit [exit]


menu()
    convert_data_to_csv()
        back_to_menu()
    split_file()
        read_data()
        export_data()
    trim_beginning()
        read_data()
        export_data()
    trim_end()
        read_data()
        export_data()
read_data()
export_data(file_out, sep=',', encoding=UTF-8)
back_to_menu() -> lance menu()

convertir en uppercase les choix
"""





"""
try:
    df = pd.read_csv(self.path, delimiter=',', dtype=float)
    print('CSV file read:', self.path)
    #print(df)
except (TypeError, ValueError, IndexError, AttributeError) as e:
    print('Error: the format of CSV file is not correct.')

print('===   PlotView trim curve for CSV files   ===')
print('This script trims a curve to keep only a defined range of this curve.')
print('The trimming range is defined by the user based on 2 values "start_index" and "end_index".')
print('These indexes can be values of X axis or values of Y axis.')

        
start_index = input('Define the value for the beginning of the range to keep (start_index): ')
try:
column = input(': X or x ')
"""

