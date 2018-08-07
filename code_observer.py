# import sys
import ast
# import os
import logging
# from constants import *
from support_methods import *


def __test_method__():
    pass


def find_py_files(from_path=None):
    if from_path == (None or ' ' or ''):
        # from_path = path_setter()
        from_path = getting_file_path(os.path.realpath(__file__))
        print from_path
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown=True):
        for file in files:
            files_list.append(filter_only_py(file, whole_path))
            if len(files_list) >= 100:
                break
    files_list = filter(None, files_list)
    logging.info('Total finded *.py files amount is: %s' % len(files_list))
    return files_list


def get_trees(files):
    trees = []
    for file in files:
        with open(file, 'r') as file_viewer:
            file_content = file_viewer.read()
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            logging.error(e)
            tree = None
        trees.append(tree)
    trees = filter(None, trees)
    logging.info('trees generated')
    return trees


def get_common_verbs(trees):
    flatten_array = flattening(only_astF_instances(trees))
    functions_list = [stringify(is_private(f)) for f in flatten_array]
    functions_list = filter(None, functions_list)
    logging.info('functions extracted')
    g = [getting_verbs(function_name) for function_name in functions_list]
    return list(flattening(g))


def cascade_call(path):
    py_files = find_py_files(path)
    trees = get_trees(py_files)
    return get_common_verbs(trees)

#
def get_common_verbs_across(projects):
    words = []
    for project in projects:
        path = os.path.join('.', project)
        words.append(cascade_call(path))
    logging.info('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in the_most_common(words):
        logging.info(word, occurence)


def cascade():
    py_files = find_py_files()
    trees = get_trees(py_files)
    return get_common_verbs(trees)

common_verbs = cascade()
print common_verbs



