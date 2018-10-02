from __future__ import print_function # so I can use Python3 syntax

# Created by: Edward Zhang, ezha210

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
                # version_file_path = os.path.join(path_dir, '.previousversions', path_file, version_file)
                versions.append(int(version_file))

        versions.sort(reverse = True)

        versionCount = 1
        for version in versions:
            print(path_file + "." + str(versionCount))
            versionCount += 1
else:
    raise Exception("Invalid path")