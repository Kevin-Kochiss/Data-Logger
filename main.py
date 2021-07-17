from csvReader import scan_files
import time
from configuration import ScriptVars, initialize

initialize()

while True:
    config      = ScriptVars()
    root_dir    = config.config['ROOT_DIR']

    if config.can_run():
        scan_rate = config.config['SCAN_RATE']
        scan_files(root_dir)
    else:
        scan_rate   = 5

    time.sleep(scan_rate)
