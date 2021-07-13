import csv
from pathlib import Path, PurePath
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
    