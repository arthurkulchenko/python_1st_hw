from support_methods import *
import logging
import os
from constants import *

def origin_find_py_files(from_path=None):
    if from_path == (None or ' ' or ''):
        from_path = path_setter()
        # from_path = getting_file_path(os.path.realpath(__file__))
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown=True):
        for file in files:
            files_list.append(filter_only_py(file, whole_path))
            if len(files_list) >= 100:
                break
    files_list = filter(None, files_list)
    logging.info('Total finded *.py files amount is: %s' % len(files_list))
    return files_list


def find_py_files(from_path=None):
    if from_path == None or ' ' or '':
        from_path = path_setter()
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown=True):
        for file in files:
            if file != None:
                files_list.append(filter_only_py(file, whole_path))
            if len(files_list) >= 100:
                break
    files_list = filter(None, files_list)
    logging.info('Total finded *.py files amount is: %s' % len(files_list))
    return files_list


f = find_py_files()
print f