# -*- coding: utf-8 -*-
""" curve_toolbox is a command line set of tools to process CSV files before plot them with PlotView.


    Code hosted at: https://github.com/fa201/PlotView
    Licence: GN GPL-3.0
"""


try:
    import csv
    import glob
    import os
    import pandas as pd
    from collections import OrderedDict
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
file_dic = OrderedDict()  # Allows to keep the order given by glob for files
status =' '


def show_title_files():
    """Clear the console, print application title and list of file
        https://www.geeksforgeeks.org/clear-screen-python/
        Detect if OS is windows or Linux
        List all CSV files for the user to see which files will be processed
        CSV files must be in 'CSV_files' folder to be detected.
        Files are sorted by name.
        Files will be selected in the menu through keys of 'file_dic'.
        'file_dic' keys are integer to ease selection through command menu.
    """
    global file_dic
    global status
    # Windows clear command
    if os.name == 'nt':
        _ = os.system('cls')
    # Linux and macOS clear command
    else:
        _ = os.system('clear')
    title = 'Curve_toolbox: prepare CSV curves for plotting with PlotView'
    print(separator)
    print(title)
    print(separator)

    # Add all CSV files in working directory into a list regardless of case for CSV extension
    temp_list_files = glob.glob('*.csv') + glob.glob('*.CSV')
    # Sort files by name
    temp_list_files = sorted(temp_list_files)

    # Reset file_dic in case the files changed while the script is running
    file_dic = {}
    # Update 'file_dic': key is a number starting at 1
    for name in temp_list_files:
        index = temp_list_files.index(name) + 1  # Get index of current list item
        file_dic[index] = name

    # Show the content of 'file_dic'
    print('')
    print('List of CSV files found in "CSV_files" folder:')
    for key in file_dic:
        print(space, key, ' -> ', file_dic[key], sep='')
    choice = 'M'

def main_commands():
    """Print the commands of the main menu"""
    print('')
    print('Main menu - commands:')
    print(space, '[C]', line, 'Convert data file to CSV format', sep='')
    print(space, '[S]', line, 'Split a CSV file into several CSV files', sep='')
    print(space, '[O]', line, 'Perform scale or shift operations on the curve', sep='')
    print(space, '[T]', line, 'Trim the beginning and or the end of the curve', sep='')
    print(space, '[L]', line, 'List CSV files', sep='')
    print(space, '[EXIT]...Exit program', sep='')

def show_main_menu(command):
    """Display main menu commands

        Commands are converted to UPPER case to ease the procesing after
        'command' defines where the commands shown are main menu, trim or split commands
    """
    global choice
    global line
    global space
    global status

    show_title_files()

    if command == 'trim':
        trim_commands()
    elif command == 'split':
        split_commands()
    elif command == 'operation':
        operation_commands()
    elif command == 'convert':
        convert_commands()
    elif command == 'main':
        main_commands()
        # Status bar
        print('')
        print('STATUS: ', status, sep='')
        print(separator)
        # Command line
        choice = input('Enter a command: ').upper()  # Converted to UPPER case to ease the procesing after
        # All code after the above will be shown only after the input is entered.

def file_head(file, dataframe):
    """Show the head of a dataframe and its file """
    print(space, 'Reading: ', file, sep='')
    print(space, 'Printing the first 5 lines of ' + file, ':', sep='')
    print(dataframe.head(5))

def trim_commands():
    """Remove all the points of the curve below or above a given values for a given column

        Export the file with the 'trim_' prefix
    """
    global space
    global file_dic
    global choice
    global status
    global space
    file_input = ''

    print('')
    #print('Warning: the CSV file to be trimmed should contain only 2 columns.')
    print('Trim menu:')
    print(space, '[M]', line, 'Go back to main menu', sep='')
    temp = input(space + 'Enter the number of CSV file to trim: ')
    # Convert file selection to upper case to simplify next if statement.
    file_input = temp.upper()

    # 'M' is entered: go back to the main menu
    if file_input == 'M':
        status = 'back to main menu.'
        choice = 'M'
        show_main_menu('main')
    # Nothing is entered: launch again the complete display for trim menu
    elif file_input =='':
        show_main_menu('trim')
    # Launch trimming.
    else:
        # CSV file reading based on 'file_dic' key.
        try:
            df_in = pd.read_csv(file_dic[int(file_input)])
            # Allow the user to check it is the selected file is the right one.
            file_head(file_dic[int(file_input)], df_in)

            # Column 1 or 2 to be considered for 'start' and 'end'
            col =''
            # Trimmed curve is delimited by 'start' and 'end'
            start = None
            end = None
            # Trimming parameter: column number, 'start' and 'end'.
            try:
                col = input(space + 'Enter the number of column to be considered [1] or [2] : ')
                if (col!='1') & (col!='2'):
                    print('ERROR 1: the number selected is not correct. It should be 1 or 2.')
                    _ = input('Press [ENTER] to continue.')
                    show_main_menu('trim')
                else:
                    # Convert to dataframe column integer index (starting at 0)
                    col = int(col) - 1
                    start = float(input(space + 'Enter the value for the start of the trimmed curve: '))
                    end = float(input(space + 'Enter the value for the end of the trimmed curve: '))
                    # Check proper order otherwise the complete points are deleted.
                    if start <= end:
                        df_in = df_in[df_in.iloc[:, col] >= start]
                        df_in = df_in[df_in.iloc[:, col] <= end]
                        # Export trimmed curve with a prefix on the file name with index column.
                        file_output = 'trimmed_' + file_dic[int(file_input)]
                        df_in.to_csv(file_output, index=False, encoding='utf-8')
                        # Update the status with trimmed curve filename
                        status = 'curve trimmed and saved as ' + file_output
                        # Display main menu since the trimming is done.
                        choice = 'M'
                        show_main_menu('main')
                    else:
                        print('ERROR 2: the start value should be lower than end value.')
                        _ = input('Press [ENTER] to continue.')
                        # Display trim menu.
                        show_main_menu('trim')
            except ValueError as e:
                print('ERROR 3: the number selected is not correct.')
                _ = input('Press [ENTER] to continue.')
                # Display trim menu
                show_main_menu('trim')

        except (ValueError, KeyError) as e:
            correct_range = str(file_dic.keys())
            correct_range = correct_range[10:-1]
            print('ERROR 4: the number selected is not in the correct range ' + correct_range + '.')
            _ = input('Press [ENTER] to continue.')
            show_main_menu('trim')

def split_commands():
    """Split a CSV file into several CSV files based on the column for X data"""
    global file_dic
    global choice
    global status
    global space
    global command
    file_input = ''

    print('')
    print('Warning: the CSV file to be split should contain more than 2 columns.')
    print('Split menu:')
    print(space, '[M]', line, 'Go back to main menu', sep='')
    temp = input(space + 'Enter the number of CSV file to split: ')
    # Convert file selection to upper case to simplify next if statement.
    file_input = temp.upper()

    # 'M' is entered: go back to the main menu
    if file_input == 'M':
        status = 'back to main menu.'
        choice = 'M'
        show_main_menu('main')
    # Nothing is entered: launch again the complete display for split menu
    elif file_input =='':
        show_main_menu('split')
    # Launch splitting.
    else:
        # CSV file reading based on 'file_dic' key.
        try:
            df_in = pd.read_csv(file_dic[int(file_input)])
            # Allow the user to check it is the selected file is the right one.
            file_head(file_dic[int(file_input)], df_in)
            if len(df_in.columns) < 3:
                print('ERROR 5: there is less than 3 columns in the file: ' + file_dic[int(file_input)] + '.')
                _ = input('Press [ENTER] to continue.')
                show_main_menu('split')
            else:
                col_x_string = ''
                message_col = 'Enter the column number to be used as X data for each CSV files'
                message_col += ' [1 , ' + str(len(df_in.columns)) + ']: '
                try:
                    col_x_string = input(space +  message_col)
                    # Shift to 0-starting column index.
                    col_x = int(col_x_string) - 1
                    if col_x not in range(0, len(df_in.columns), 1):
                        max_range = str(len(df_in.columns))
                        print('ERROR 6: the selected file column is not in the correct range [1 , ' + max_range + '].')
                        _ = input('Press [ENTER] to continue.')
                        # Display trim menu to remove the error from display.
                        show_main_menu('split')
                    else:
                        i = 0
                        for index in df_in.columns:
                            #print('[df_in.iloc[:, col_x]]: ', [df_in.iloc[:, col_x]])
                            #print('df_in[index]: ', df_in[index])
                            if index != df_in.columns[col_x]:
                                df_temp = pd.concat([df_in.iloc[:, col_x], df_in[index]], axis=1, join='outer')
                                i += 1
                                # Remove CSV extension on file name, add file number and add back CSV extension name
                                file_output = file_dic[int(file_input)][:-4] + '_' + str(i) + '.csv'
                                df_temp.to_csv(file_output, index=False, encoding='utf-8')
                            else:
                                # This dataframe is not interesting
                                pass
                        # Update the status with trimmed curve filename
                        status = 'curves split and saved, check the list of files'
                        # Display the main menu since the splitting is done.
                        choice = 'M'
                        show_main_menu('main')
                except (ValueError, KeyError) as e:
                    max_range = str(len(df_in.columns))
                    print('ERROR 7: the selected file column is not in the correct range [1 , ' + max_range + '].')
                    _ = input('Press [ENTER] to continue.')
                    show_main_menu('split')
        except (ValueError, KeyError) as e:
            correct_range = str(file_dic.keys())
            correct_range = correct_range[10:-1]
            print('ERROR 8: the selected file number is not in the correct range ' + correct_range + '.')
            _ = input('Press [ENTER] to continue.')
            show_main_menu('split')

def operation_commands():
    """Perform scale or shift operation on the curve"""
    global file_dic
    global choice
    global status
    global space
    global command
    file_input = ''

    print('')
    print('Scale = multiply by a given number all values of X or Y axis of the curve.')
    print('Shift = add a given number to all values of X or Y axis of the curve.')
    print('Operation menu:')
    print(space, '[M]', line, 'Go back to main menu', sep='')
    temp = input(space + 'Enter the number of CSV file to split: ')
    # Convert file selection to upper case to simplify next if statement.
    file_input = temp.upper()

    # 'M' is entered: go back to the main menu
    if file_input == 'M':
        status = 'back to main menu.'
        choice = 'M'
        show_main_menu('main')
    # Nothing is entered: launch again the complete display for split menu
    elif file_input =='':
        show_main_menu('operation')
    # Launch operation.
    else:
        # CSV file reading based on 'file_dic' key.
        try:
            df_in = pd.read_csv(file_dic[int(file_input)])
            # Allow the user to check it is the selected file is the right one.
            file_head(file_dic[int(file_input)], df_in)
            if len(df_in.columns) > 2:
                print('Warning: this file has more than 2 columns. Only the first 2 columns will be modified.')
            scale_x = ''
            scale_y = ''
            shift_x = ''
            shift_y = ''

            # Get x scale factor or use default value given by enter
            scale_x = float(input('Enter the scale factor for X data [1.0]: ') or '1.0')
            scale_y = float(input('Enter the scale factor for Y data [1.0]: ') or '1.0')
            shift_x = float(input('Enter the shift value factor for X data [0.0]: ') or '0.0')
            shift_y = float(input('Enter the shift value factor for Y data [0.0]: ') or '0.0')
            
            # Forbids scale factors equal to 0
            if scale_x == 0 or scale_y == 0:
                print('ERROR 9: the scale factor cannot be 0.')
                _ = input('Press [ENTER] to continue.')
                show_main_menu('operation')
            else:
                df_in.iloc[:, 0] = df_in.iloc[:, 0] * scale_x + shift_x
                df_in.iloc[:, 1] = df_in.iloc[:, 1] * scale_y + shift_y
                file_output = 'operation_' + file_dic[int(file_input)]
                df_in.to_csv(file_output, index=False, encoding='utf-8')
                # Update the status with trimmed curve filename
                status = 'operations are done and the curve is saved as ' + file_output
                # Display main menu since the trimming is done.
                choice = 'M'
                show_main_menu('main')
        except ValueError as e:
            print('ERROR 10: a number should be entered.')
            _ = input('Press [ENTER] to continue.')
            show_main_menu('operation')

def convert_commands():
    """Convert input file into CSV strict format"""
    global file_dic
    global choice
    global status
    global space
    global command
    file_input = ''

    print('')
    print('Attempt to convert the input file into strict CSV format.')
    print('Convert menu:')
    print(space, '[M]', line, 'Go back to main menu', sep='')
    temp = input(space + 'Enter the number of CSV file to read: ')
    # Convert file selection to upper case to simplify next if statement.
    file_input = temp.upper()

    # 'M' is entered: go back to the main menu
    if file_input == 'M':
        status = 'back to main menu.'
        choice = 'M'
        show_main_menu('main')
    # Nothing is entered: launch again the complete display for split menu
    elif file_input =='':
        show_main_menu('convert')
    # Launch splitting.
    else:
        # CSV file reading based on 'file_dic' key.
        print('Python CSV sniffer attempts to determine the CSV dialect.')
        try:
            with open(file_dic[int(file_input)], 'r') as file_in:
                # Read 1024 characters to determine dialect attributes
                sample = file_in.read(2000)
                dial = csv.Sniffer().sniff(sample)
            print('"CSV Dialect" parameters are written between > and <:')
            print('Separator: >', dial.delimiter, '<', sep='')
            print('Doublequote: >', dial.doublequote, '<', sep='')
            print('Escapechar: >', dial.escapechar, '<', sep='')   
            #print('Lineterminator: >', dial.lineterminator, '<', sep='')
            print('Quotechar: >', dial.quotechar, '<', sep='')
            print('Skipinitialspace after separator: >', dial.skipinitialspace, '<', sep='')
            _ = input('Press [ENTER] to continue.')
            # Use dialect attributes as input for read_csv.
            df_in = pd.read_csv(file_dic[int(file_input)], dialect=dial)
            # Show the begining of datatrame.
            file_head(file_dic[int(file_input)], df_in)
            _ = input('Press [ENTER] to continue.')
            # Write CSV file in UTF-8
            file_output = 'convert_' + file_dic[int(file_input)]
            df_in.to_csv(file_output, index=False)
            status = 'CSV file is converted and saved as ' + file_output
            # Display main menu since the trimming is done.
            choice = 'M'
            show_main_menu('main')
        except:
            print('ERROR 10: CSV sniff attempt failed.')
            print('Try to convert this file with a spreadsheet (MS-Excel, LibreOffice Calc, etc).')
            _ = input('Press [ENTER] to continue.')
            status = 'CSV file conversion failed.'
            # Display main menu since the trimming is done.
            choice = 'M'
            show_main_menu('main')


# Main program
show_main_menu('main')
while choice != 'EXIT':
    if choice == 'M':
        # Display main menu
        status = ''
        show_main_menu('main')

    elif choice == 'C':
        show_main_menu('convert')

    elif choice == 'S':
        # Display split menu
        show_main_menu('split')

    elif choice == 'O':
        # Display operation menu
        show_main_menu('operation')

    elif choice == 'T':
        # Display trim menu
        show_main_menu('trim')

    elif choice == 'L':
        status = 'the list of files was updated.'
        # No need to display list menu since the list is updated for all menus.
        show_main_menu('main')

    else:
        status = 'unknown command. The list of command is shown above.'
        show_main_menu('main')
print('\nExiting the program.')
