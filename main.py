from csvReader import scan_files
import time

ROOT_DIR = ''
SCAN_RATE = 300

while True:
    scan_files(ROOT_DIR)
    time.sleep(SCAN_RATE)