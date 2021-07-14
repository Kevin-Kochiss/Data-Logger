import csv
from pathlib import Path
from itertools import zip_longest
import re

class ScriptVars():
    def __init__(self):
        if not self.CONFIG_DIR.exists():
             Path.mkdir(self.CONFIG_DIR)
        self.read_vars()

    def read_vars(self):
        try:
            with open(self.SETTINGS_FILE, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                new_dict = {key:row[1] for key, row in zip_longest(self.var_dict, csv_reader)}
                self.var_dict = self.clean_dict(new_dict)
                
        except IOError:
            with open(self.SETTINGS_FILE, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                for key, value in self.var_dict.items():
                    csv_writer.writerow([key, value])
    
    def clean_dict(self, in_dict):
        if not Path(in_dict['ROOT_DIR']).exists():
            in_dict['ROOT_DIR'] = self.var_dict['ROOT_DIR']
        scan_rate = clean_int(in_dict['SCAN_RATE'])
        if not scan_rate >= 1 or scan_rate <= 3600:
            in_dict['SCAN_RATE'] = self.var_dict['SCAN_RATE']

        return in_dict

    def get_vars(self):
        return self.var_dict
    
    var_dict = {
        'ROOT_DIR': 'Path',
        'SCAN_RATE': 300,
        }
    CONFIG_DIR      = Path.joinpath(Path(__file__).parent.absolute(), 'config')
    MANIFEST_FILE   = Path.joinpath(CONFIG_DIR, 'manifest.txt')
    SETTINGS_FILE   = Path.joinpath(CONFIG_DIR, 'settings.csv')
    EMAIL_ADDRESS   = ''
    EMAIL_PASS      = ''
    
def clean_int(val):
    return re.sub('[^0-9]', '', val)


my_vars = ScriptVars()

print(my_vars.CONFIG_DIR)

# r_list= [1,2,3]
# r_dict= {'a':30, 'b':'two'}
# print(isinstance(r_dict['a'], int))
# new_dict = {key:row for key, row in zip_longest(r_dict, r_list)}
# print(new_dict)

# with open('settings.csv', 'r') as f:
#     csv_reader = csv.reader(f)
#     new_dict = {key:row[1] for key, row in zip_longest(my_vars.var_dict, csv_reader)}
#     print(new_dict)
#     print(isinstance(new_dict['SCAN_RATE'], str))
#     print(clean_int(new_dict['SCAN_RATE']))