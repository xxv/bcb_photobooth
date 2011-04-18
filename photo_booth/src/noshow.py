#!/usr/bin/python

import pexpect, re
import os, sys

import urllib

import subprocess

unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stdout = unbuffered

subprocess.call(["adb", "logcat", "-c"])
child = pexpect.spawn('adb logcat -s DecodeHandler:D', timeout=10000)
find_code = re.compile(r'D/DecodeHandler\([^)]+\): (.*)')
while not child.eof():
    child.expect(find_code)
    scan = child.match.group(1)
    if scan.startswith('Found barcode'):
        continue
    print scan
