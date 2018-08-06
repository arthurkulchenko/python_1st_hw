import ast
import os
from constants import Path
import custom_methods
import logging


def flattening(array):
    custom_methods.flattening(array)


def is_verb(array=None):
    custom_methods.is_verb(array)


def is_none_filter(array):
    custom_methods.is_none_filter(array)


def filter_only_py_extention(file, from_path):
    custom_methods.filter_only_py_extention(file, from_path)


def is_ast_Function_instance_filter(node):
    custom_methods.is_ast_Function_instance_filter(node)


def the_most_common(objects, top_size=10):
    custom_methods.the_most_common(objects, top_size=10)


def find_py_files(from_path=Path):
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown=True):
        for file in files:
            files_list.append(filter_only_py_extention(file, whole_path))
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
            print(e)
            tree = None
        trees.append(tree)
    logging.info('trees generated')
    return trees


def __test_method__():
    print "Hello"


def is_private_filter_and_stringify(thing):
    if type(thing).__name__.startswith('__'):
        if type(thing).__name__.endswith('__'):
            print thing.__class__.__name__
            return "%s" % thing.__class__.__name__


def get_common_verbs(trees):
    flatten_array = flattening(is_none_filter(trees))
    functions_list = [is_private_filter_and_stringify(f) for f in flatten_array]
    functions_list = filter(None, functions_list)
    logging.info('functions extracted')
    g = flattening([getting_verbs(function_name) for function_name in functions_list])
    return list(g)


def cascade_call(path):
    py_files = find_py_files(path)
    trees = get_trees(py_files)
    return get_common_verbs(trees)


def get_common_verbs_across(projects):
    words = []
    for project in projects:
        path = os.path.join('.', project)
        words.append(cascade_call(path))
    logging.info('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in the_most_common(words):
        logging.info(word, occurence)


def getting_verbs(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]
