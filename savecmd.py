#!/usr/bin/python3
# save a bash command to bin dir

import subprocess
import argparse
import os
from pathlib import Path

BINDIR = os.environ['HOME'] + '/bin'

parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()

name = args.name[0]
postfix = ''

if not name.endswith('.sh'):
    postfix = '.sh'

p = Path(BINDIR + '/'+ args.name + postfix)

if p.exists():
    print('File %s already exists.' % (p.name))
    exit(1)

with p.open('w') as file:
    file.write('#!/bin/bash\n')
    file.write(' '.join(args.command) + '\n')

p.chmod(0o755)
