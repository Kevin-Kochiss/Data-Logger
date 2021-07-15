import csv
from os import write
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
                new_dict = {key:row[1] for key, row in zip_longest(self.config, csv_reader)}
                self.config = self.clean_dict(new_dict)
                
        except IOError:
            self.write_settings(self.config)
    
    def clean_dict(self, in_dict):
        failed = False
        if not Path(in_dict['ROOT_DIR']).exists():
            in_dict['ROOT_DIR'] = self.config['ROOT_DIR']
            failed = True

        scan_rate = clean_int(in_dict['SCAN_RATE'])
        if scan_rate < 1 or scan_rate > 3600:
            in_dict['SCAN_RATE'] = self.config['SCAN_RATE']
            failed = True
        
        if failed:
            self.write_settings(in_dict)

        return in_dict

    def write_settings(self, in_dict):
        with open(self.SETTINGS_FILE, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                for key, value in in_dict.items():
                    csv_writer.writerow([key, value])
    
    config = {
        'ROOT_DIR': 'Path',
        'SCAN_RATE': 120,
        }
    CONFIG_DIR      = Path.joinpath(Path(__file__).parent.absolute(), 'config')
    MANIFEST_FILE   = Path.joinpath(CONFIG_DIR, 'manifest.txt')
    SETTINGS_FILE   = Path.joinpath(CONFIG_DIR, 'settings.csv')
    RECIPIENTS      = Path.joinpath(CONFIG_DIR, 'recipients.csv')
    EMAIL_ADDRESS   = 'lubrizoldatalogger@gmail.com'
    EMAIL_PASS      = 'rccfnclgvmcjgrdv'
    
    
def clean_int(val):
    return int(re.sub('[^0-9]', '', val))
    

