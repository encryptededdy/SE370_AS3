from __future__ import print_function # so I can use Python3 syntax

import os
import sys
import time

if len(sys.argv) != 2:
    raise Exception("Expected one argument (file path)")
elif os.path.exists(str(sys.argv[1])):
    (path_dir, path_file) = os.path.split(str(sys.argv[1]))
    existing_version_count = 0
    if not os.path.exists(os.path.join(path_dir, '.previousversions', path_file)):
        print("No previous versions found")
    else:
        versions = []
        for version_file in os.listdir(os.path.join(path_dir, '.previousversions', path_file)):
            if version_file.isdigit():
                version_file_path = os.path.join(path_dir, '.previousversions', path_file, version_file)
                versions.append("Version " + version_file + ", modified " + time.ctime(os.path.getmtime(version_file_path)))

        versions.sort()

        for version in versions:
            print(version)
else:
    raise Exception("Invalid path")