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
                version_file_path = os.path.join(path_dir, '.previousversions', path_file, version_file)
                versions.append(version_file_path)

        versions.sort(reverse = True)

        versions.pop(0) # pop off the first entry, as that's the current version.
        for version in versions:
            os.remove(version) # delete all the others

else:
    raise Exception("Invalid path")