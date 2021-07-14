from csvReader import scan_files
import time
from configuration import ScriptVars

config_vars = ScriptVars()
root_dir = config_vars.config['ROOT_DIR']
scan_rate = config_vars.config['SCAN_RATE']

while True:
    scan_files(root_dir)
    time.sleep(scan_rate)