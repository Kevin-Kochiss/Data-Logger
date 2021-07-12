import csv
file_path   = ''
file_name    = ''

## Main loop
with open(file_name, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    #### read rows
    #### write them to a sepreate csv label with with a batch number
    #### 
    string = 'test'