from __future__ import print_function # so I can use Python3 syntax

# Created by: Edward Zhang, ezha210

import os
import sys
import time

if len(sys.argv) != 3:
    raise Exception("Expected two arguments (file path, version)")
elif os.path.exists(str(sys.argv[1])):
    (path_dir, path_file) = os.path.split(str(sys.argv[1]))
    existing_version_count = 0
    if not os.path.exists(os.path.join(path_dir, '.previousversions', path_file)):
        print("No previous versions found")
    else:
        foundVersion = False
        for version_file in os.listdir(os.path.join(path_dir, '.previousversions', path_file)):
            if version_file.isdigit() and int(version_file) == int(sys.argv[2]):
                # found the version!
                f = open(os.path.join(path_dir, '.previousversions', path_file, version_file), 'r')
                print(f.read())
                f.close()
                foundVersion = True
        if not foundVersion:
            raise Exception("Version number doesn't exist")

else:
    raise Exception("Invalid path")