#!/usr/bin/python

import re, sys
import subprocess

#baseurl = "http://127.0.0.1:8000/"
baseurl = "http://faces.barcampboston.org/"

ebid_file = re.compile(r'ebid(\d+)\.jpg')
if __name__ == '__main__':
    for filename in sys.argv[1:]:
        m = ebid_file.match(filename)
        if not m:
            sys.stderr.write("not processing %s\n" % filename)
            continue
        ebid = m.group(1)
        url = "%sattendee/ebid:%s/photo" % ( baseurl, ebid)
        print "Uploading %s to %s ..." % ( filename, url)
        subprocess.call(["curl", "-s", "-o", "/dev/null", "-F", "photo=@%s" % filename, url])

