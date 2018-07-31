import ast
import os
import collections
from nltk import pos_tag, word_tokenize, punkt
import constants
import custom_methods

def flattening(array):
    custom_methods.flattening(array)

def is_verb(array = None):
    custom_methods.is_verb(array)

def is_none_filter(array):
    custom_methods.is_none_filter(array)

def filter_only_py_extention(file, from_path):
    custom_methods.filter_only_py_extention(file, from_path)
# SEARCHING
def find_py_files(from_path = Path):
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown = True):
        for file in files:
            files_list.append(filter_only_py_extention(file, whole_path))
            if len(files_list) >= 100:
                break
    files_list = filter(None, files_list)
    print('Total finded *.py files amount is: %s' % len(files_list))
    return files_list
# SEARCHING
def get_trees(files, with_files = False, with_file_content = False):
    trees = []
    for file in files:
        with open(file, 'r') as file_viewer:
            file_content = file_viewer.read()
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_files:
            if with_file_content:
                trees.append((file, file_content, tree))
            else:
                trees.append((file, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees
# OPERATOIN AT FUNCTION NAMES
def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]

def is_private_filter_and_stringify(thing):
    if True:
    # FIX no clearly understood conditions 
    # if thing.__class__.__name__.startswith('__') and thing.__class__.__name__.endswith('__'):
        # print thing.__class__.__name__
        return "%s" %thing.__class__.__name__
# FILTER OF A AST OBJECTS
def is_astFunction_instance_filter(node):
    if isinstance(node, ast.FunctionDef):
        return node.name.lower()

def get_common_verbs(trees):
    flatten_array = flattening(is_none_filter(trees))
    fncs = [is_private_filter_and_stringify(f) for f in flatten_array]
    fncs = filter(None, fncs)
    print('functions extracted')
    return flattening([get_verbs_from_function_name(function_name) for function_name in fncs])

def the_most_common(objects, top_size=10):
    return collections.Counter(objects).most_common(top_size)

def cascade_call(path):
    py_files = find_py_files(path)
    trees = get_trees(py_files)
    return get_common_verbs(trees)
# NOT FINISHED
def get_common_verbs_across(path, projects):
    words = []
    for project in projects:
        # path = os.path.join('.', project)
        words.append(cascade_call(path))
    print('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in the_most_common(words):
        print(word, occurence)

# UNUSED
def get_all_names(trees):
    for t in trees:
        names = [ node.id for node in ast.walk(t) if isinstance(node, ast.Name)]
    return filter(None, names)

def puts(smth):
    print smth
#
# def split_snake_case_name_to_words(name):
#     return [n for n in name.split('_') if n]
#     return flattening([split_snake_case_name_to_words(function_name) for function_name in function_names])
    


