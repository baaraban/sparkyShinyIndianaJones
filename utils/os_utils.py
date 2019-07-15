import os
import re


def get_files_rec(regex, folder=os.getcwd()):
    result = []
    for (dir_path, dir_names, filenames) in os.walk(folder):
        for file in filenames:
            if re.match(regex, file):
                result.append(f"{dir_path}\{file}")
    return result
