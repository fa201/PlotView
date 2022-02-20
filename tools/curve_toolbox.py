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
# GLOBAL VARIABLES
# Choice of command for the main menu
choice = 'M'
# Parameters for display variables
separator = '~'*60
line = '.' * 6
space = ' ' * 3
file_dic = {}
status =' '
command ='main'

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
    #print('=' * len(title))  # Generate a line with the same width as the title
    print(separator)
    print(title)
    print(separator)

def main_commands():
    """Print the commands of the main menu"""
    print('')
    print('Main menu - commands:')
    print(space, '[C]', line, 'Convert data file to CSV format', sep='')
    print(space, '[S]', line, 'Split a CSV file into several CSV files', sep='')  # uniquement pour les fichiers partageant le même X
    print(space, '[T]', line, 'Trim the beginning and or the end of the curve', sep='')
    print(space, '[L]', line, 'List CSV files', sep='')
    print(space, '[EXIT]...Exit program', sep='')

def show_main_menu():
    """Display main menu commands

        Commands are converted to UPPER case to ease the procesing after
    """
    global choice
    global line
    global space
    global status
    global command

    clear_console()
    show_title()
    list_files()

    if command == 'trim':
        trim_commands()
    elif command == 'main':
        main_commands()
        # Status bar
        print('')
        print('STATUS: ', status, sep='')
        print(separator)
        # Command line
        choice = input('Enter a command: ').upper()
        # All code after the above will be shown only after the input is entered.

def reset_choice():
    """Reset choice to empty string to avoid an error in show_main_menu"""
    global choice
    choice = 'M'

def list_files():
    """List all CSV files for the user to see which files will be processed

        CSV files must be in 'CSV_files' folder to be detected.
        Files will be selected in the menu through keys of 'file_dic'.
        'file_dic' keys are integer to ease selection through command menu.
    """
    global file_dic
    global status
    # Add all CSV files in working directory into a list
    temp_list_files = glob.glob('*.csv')

    # Update 'file_dic': key is a number starting at 1
    for name in temp_list_files:
        index = temp_list_files.index(name) + 1  # Get index of current list item
        file_dic[index] = name

    # Show the content of 'file_dic'
    print('')
    print('List of CSV files found in "CSV_files" folder:')
    for key in file_dic:
        print(space, key, ' -> ', file_dic[key], sep='')
    reset_choice()

def trim_commands():
    """Remove the point of the curve before or after given values

        Export the file with the 'trim_' prefix
    """
    global space
    global file_dic
    global choice
    global status
    global space
    global command
    file_input = ''

    print('')
    print('Warning: the CSV file to be trimmed should contain only 2 columns')
    print('Trim menu:')
    print(space, '[M]', line, 'Go back to main menu', sep='')
    temp = input(space + 'Enter the number of CSV file to trim: ')
    # Convert to upper to simplify next if statement.
    file_input = temp.upper()

    if file_input == 'M':
        global command  # necessary as the namespace if different from above
        command = 'main'
        status = 'back to main menu.'
        reset_choice()
        show_main_menu()
    elif file_input =='':
        # Launch again the complete display for title, list of files and trim commands
        clear_console()
        show_title()
        list_files()
        trim_commands()
    else:
        try:
            print(space, 'Reading: ', file_dic[int(file_input)], sep='')
            df_in = pd.read_csv(file_dic[int(file_input)])
            print('Printing the first 5 lines of ' + file_dic[int(file_input)])
            print(df_in.head(5))
        except ValueError as e:
            correct_range = str(file_dic.keys())
            correct_range = correct_range[10:-1]
            print('The number selected is not in the correct range ' + correct_range + '. Try again.')
            trim_commands()
        except KeyError as e:
            correct_range = str(file_dic.keys())
            correct_range = correct_range[10:-1]
            print('The number selected is not in the correct range ' + correct_range + '. Try again.')
            trim_commands()
        # Column 1 or 2 to be considered for 'start' and 'end'
        col =''
        # Trimmed curve is delimited by 'start' and 'end'
        start = None
        end = None
        col = input(space + 'Enter the number of column to be considered [1] or [2] : ')
        #try:
        col = int(col) - 1  # convert to dataframe column integer index
        #except:
        start = float(input(space + 'Enter the value for the start of the trimmed curve: '))
        df_in = df_in[df_in.iloc[:, col] >= start]
        end = float(input(space + 'Enter the value for the end of the trimmed curve: '))
        df_in = df_in[df_in.iloc[:, col] <= end]
        # Export trimmed curve with a prefix on the file name
        file_output = 'trimmed_' + file_dic[int(file_input)]
        df_in.to_csv(file_output, index=False)
        # Update the status with trimmed curve filename
        status = 'curve trimmed and saved as ' + file_output

        # Go back to main menu
        reset_choice()
        command = 'main'
        show_main_menu()


# Main program
show_main_menu()
while choice != 'EXIT':
    if choice == 'M':
        status = ''
        show_main_menu()

    elif choice == 'C':
        show_main_menu()

    elif choice == 'S':
        show_main_menu()

    elif choice == 'T':
        command = 'trim'
        show_main_menu()

    elif choice == 'L':
        status = 'the list of files was updated.'
        command = 'main'
        show_main_menu()

    else:
        status = 'unknown command. The list of command is shown above.'
        command = 'main'
        show_main_menu()
print('\nExiting the program.')

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
Trim the beginning of the curve [B]

Trim the end of the curve [E]
    Export en file_end.csv

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
export_data(file_out, sep=',', encoding=UTF-8)
back_to_menu() -> lance menu()
"""
