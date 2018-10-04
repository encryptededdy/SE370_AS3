from __future__ import print_function # so I can use Python3 syntax

# Created by: Edward Zhang, ezha210

import os
import shutil
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
        versions = []
        for version_file in os.listdir(os.path.join(path_dir, '.previousversions', path_file)):
            if version_file.isdigit():
                # version_file_path = os.path.join(path_dir, '.previousversions', path_file, version_file)
                versions.append(int(version_file))

        versions.sort(reverse=True)

        if int(sys.argv[2]) <= 6 and int(sys.argv[2]) <= len(versions) and int(sys.argv[2]) > 0:
            file_number = str(versions[int(sys.argv[2]) - 1])
            source = os.path.join(path_dir, '.previousversions', path_file, file_number)
            dest = str(sys.argv[1])
            shutil.copyfile(source, dest)

        else:
            raise Exception("Version number doesn't exist / is invalid")
else:
    raise Exception("Invalid path")