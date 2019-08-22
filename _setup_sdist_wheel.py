#!/usr/bin/env python

import os
import sys
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))

# Create new distributable files
args = [sys.executable, "setup.py", "sdist", "bdist_wheel"]
returncode = subprocess.call(args, cwd = THISDIR)
if returncode != 0:
    input("Press ENTER to continue...")
