from itertools import zip_longest
import csv
import time
from datetime import datetime
import os
from pathlib import Path
from configuration import ScriptVars
from email_dispatch import send_batch_email

# This module is responsible for scanning through the folder directory
# and detecting new files, monitoring them until data capture is 
# complete before passing them off to the email module

def scan_files(root_dir):
    '''
    This function scans through the files of the root directory.
    If the root_dir does not exist it exits, allowing for the user to update it
    '''
    config = ScriptVars()
    if not Path(root_dir).exists:
        if config.can_debug:
            print('Provided ROOT_DIR does not exist:\n{}'.format(root_dir))
        return
    
    walk_dir(root_dir)

def walk_dir(directory):
    if not Path(directory).exists():
        if ScriptVars().can_debug:
            print('Provided directory does not exist:\n{}'.format(directory))
        return
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            monitor_data(path)
        elif os.path.isdir(path):
            walk_dir(path)
    
def monitor_data(file_path):
    '''
    Reads the file located at the provided path, verifies the format is correct
    and monitors the run, emailing the csv once completed
    '''
    ext = os.path.splitext(file_path)[-1].lower()
    if ext != '.csv':
        return
    config = ScriptVars()
    manifest_path = config.MANIFEST_FILE
    manifest_content = config.get_or_create_manifest()
    #manifest_content = get_or_create_manifest(manifest_path)
    if file_path in manifest_content:
        return

    if config.can_debug:
            print('Valid file found at:\n{}'.format(file_path))
    time_1              = None
    time_2              = None
    scanning_rate       = config.config['MIN_SWEEP']
    passes_unchanged    = 0
    data_points         = 0
    while True:
        try:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Dynamically adjusts the scanning rate
                if time_1 == None and data_points > 3:
                    for row in csv_reader:
                        if row[0].strip().isdigit():
                            if time_1 == None:
                                time_1 = row[1]
                                continue
                            if time_2 == None:
                                time_2 = row[1]
                                break
                            
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
            #email_errors('FILE_READ')

        if time_1 != None and time_2 != None:
            result = subtract_times(time_1.split(' ')[-1], time_2.split(' ')[-1])
            if result > scanning_rate:
                scanning_rate = result
        time.sleep(scanning_rate)
        #if no change in data_points after two passes, the log is complete break
        if passes_unchanged == 2:
            break

    if send_batch_email(attachments=file_path):
        pass #Generate error report txt
    update_manifest(file_path)

def subtract_times(time_1, time_2):
    '''Substracts two times in HH:MM:SS and retruning the difference in seconds'''
    from itertools import zip_longest 
    time_1 = time_1.split(':')
    time_2 = time_2.split(':')

    delta_seconds = 0
    index = 0
    for t1,t2 in zip_longest(time_1, time_2, fillvalue=0): 
        dif = abs(int(t1)-int(t2))
        delta_seconds += dif * 3600 / (60**index)
        index += 1
    return delta_seconds

def update_manifest(in_path):
    '''This function updates the manifest file with a new entry'''
    manifest_path = ScriptVars().MANIFEST_FILE
    with open(manifest_path, 'a') as manifest_file:
        manifest_entry = '{}\t{}\n'.format(
            datetime.now().strftime('%x'),in_path)
        manifest_file.write(manifest_entry)
    clean_manifest()

def clean_manifest():
    manifest_path = ScriptVars().MANIFEST_FILE
    with open(manifest_path, 'r+') as manifest_file:
        entries = manifest_file.read()
        entries = entries.splitlines()
        manifest_file.seek(0)
        print(entries)
        entries = [entry for entry in entries if check_date(entry)]
        print('Joined:\n {}'.format('\n'.join(entries)))
        for entry in entries:
            manifest_file.write('{}\n'.format(entry))
        #manifest_file.write('\n'.join(entries))
        manifest_file.truncate()

def check_date(entry):
    entry = entry.split('\t')
    dif = datetime.strptime(entry[0], '%x') - datetime.now()
    if dif.days > 7:
        base_path = Path(entry[1])
        file_paths = [base_path]
        ccr_path = os.path.splitext(base_path)[0] + '.ccr'
        file_paths.append(Path(ccr_path))
        png_path = os.path.splitext(base_path)[0] + '.png'
        file_paths.append(Path(png_path))
        for fp in file_paths:
            if fp.exists():
                os.remove(fp)
        return False
    else:
        return True

def get_or_create_manifest(path):
    try:
        with open(path, 'r') as manifest:
            manifest_content = manifest.read()
    except:
        with open(path, 'w') as manifest:
            manifest_content = ''
            manifest.write(manifest_content)
    return manifest_content
