#!/usr/bin/python3
# look for chages in directory or file and run command if change detected

from pathlib import Path
from time import sleep
import argparse
import logging
import subprocess
import os
import sys

#logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('directory')
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()

dir = Path(args.directory)

if not dir.exists():
    logging.error('Directory not found.')
    exit(1)
    
files = {}

def run_command(cmd):
    c = Path(cmd[0])
    retry = True
    while retry:
        try:
            subprocess.run(cmd)
            retry = False
        except:
            logging.info('Command %s not working. Trying again.', cmd)
        sleep(1)

def has_changed(path, filestate):
    changed = False
    files = []
    
    if path.is_dir():        
        for i in path.iterdir():
            files.append(i)
    else:
        files.append(path)
        
    for f in files:
        mtime_was = filestate.get(f.name)
        if mtime_was:
            try:
                mtime_now = f.stat().st_mtime
            finally:
                if mtime_was != mtime_now:
                    logging.info('File %s changed.' % (f.name))
                    changed = True                    
        try:
            filestate[f.name] = f.stat().st_mtime
        except:
            pass
    return changed

while 1:
    changed = False
    if has_changed(dir, files):
        run_command(args.command)
        has_changed(dir, files) # update file list
    sleep(1)
