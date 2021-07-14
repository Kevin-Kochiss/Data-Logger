import csv
import re
import time
from pathlib import Path
## Main loop
#Access the manifest log to see what file should be accessed, ie if a new file has been created
my_file_path = Path(r'C:\Users\kevin\Documents\graphtec\GL100_240_840-APS\Data\2021-07-12\GL240_DEMO_01_2021-07-12_12-53-13.csv')
if my_file_path.exists():
    with my_file_path.open('r') as csvfile:
        csvreader = csv.reader(csvfile)
        #### read rows
        #Frind row containign <Row 17> 'Data', split the list there, the trunk of that list will start with headers, row after that is units, row after that starts data
        #fields = next(csvreader)
        row_num = 0
        for row in csvreader:
            row_num += 1
            #print("Row {}: {}")
            print("Row {}: {}".format(row_num, row))
            print('Test')
            # for col in row:
                # move move col into approriate var
        #### write them to a sepreate csv label with with a batch number


# This module is responsible for scanning through the folder directory
# and detecting new files, monitoring them until data capture is 
# complete before passing them off to the email module

def scan_files(root_dir):
    pass

def monitor_data(file_path):
    #default & minimum sleep rate of 1 second, which is then adjusted after esatblishing the differnce in two points
    #from the csv
    sampling_rate   = -1
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row[0] == 'Sampling':
                    sampling_rate = re.sub('[^0-9]', '', row[1])
        if sampling_rate == -1:
            sampling_error(file_path)
            return

    except(IOError, EOFError) as e:
        print("Testing multiple exceptions. {}".format(e.args[-1]))
        email_errors('FILE_READ')

    while True:
        passes_unchanged = 0
        data_points     = 0
        try:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row[0] == 'Total data points':
                        new_data_points = int(row[1])
                        if new_data_points == data_points:
                            passes_unchanged += 1
                        else:
                            data_points = new_data_points
                        break
        except(IOError, EOFError) as e:
            print("Testing multiple exceptions. {}".format(e.args[-1]))
            email_errors('FILE_READ')

        time.sleep(sampling_rate * 10)
        #if no change in data_points after two passes, break
        if passes_unchanged == 2:
            break

    email_data()

def email_data():
    pass

def email_errors(error_string):
    if(error_string == 'SAMPLING_RATE'):
        error_message = 'An error was detected when attempting to read a file'

def sampling_error(file_path):
    error_msg = 'An error was detected when attempting to read:\n\n{}\n\n'\
        .format(file_path)
    error_msg += 'The sampling rate was not detected on the file.'\
        '\"Sampling\" was not found as a cell item.'\
        'Check to see if this file is the correct type'
    email_errors(error_msg)