import os
import ast
import sys
import logging
from support_methods import *

logging.basicConfig(level = logging.INFO)


def __test_method__():
    pass


def find_py_files(from_path=None):
    if from_path == None or ' ' or '':
        from_path = path_setter()
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
            logging.error("%s in get_trees method." % e)
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
    result = get_common_verbs(trees)
    logging.info(result)
    return result

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
    verbs = get_common_verbs(trees)
    logging.info(the_most_common_of(verbs))
    return the_most_common_of(verbs)


def switch_case_1():
    dictionary = {
        "-c": "cascade()",
        "-h": "help_dialog()"
    }
    return dictionary


def functionality(key):
    dictionary = switch_case_1()
    args = args_handler(key)
    args_length = len(args)
    if args_length >= 2:
        eval(dictionary[stringify(args[1])])
    elif args_length == 1:
        help_dialog()
    
def help_dialog():
    print "Hello I am a helper \n\n -h :call this helper \n -c :call the most common verbs in *py files"

    

functionality(sys.argv)










