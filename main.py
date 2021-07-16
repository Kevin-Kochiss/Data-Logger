from csvReader import scan_files
import time
from configuration import ScriptVars

with ScriptVars() as sc:
    sc.get_or_create_recipients()

while True:
    config = ScriptVars()
    root_dir = config.config['ROOT_DIR']
    scan_rate = config.config['SCAN_RATE']
    if config.can_run():
        scan_files(root_dir)
    time.sleep(scan_rate)