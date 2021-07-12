import csv
from pathlib import Path


## Main loop
#Access the manifest log to see what file should be accessed, ie if a new file has been created
my_file_path = Path(r'C:\Users\kevin\Documents\graphtec\GL100_240_840-APS\Data\2021-07-11.csv')
print(my_file_path)
with open(my_file_path, 'r') as csvfile:
    print('Hello')
    csvreader = csv.reader(csvfile)
    #### read rows
    #fields = next(csvreader)
    row_num = 0
    for row in csvreader:
        row_num += 1
        #print("Row {}: {}")
        for col in row:
            print("Row {}: ".format(row_num))
            print("%10s"%col),
            print('\n')
    #### write them to a sepreate csv label with with a batch number
    