import ast
import os
import collections
from nltk import pos_tag, word_tokenize, punkt
import constants

# OPERATION AT LISTS
def flattening(l):
    if type(l) == 'List':
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in flattening(el):
                    yield sub
            else:
                yield el
    else:
        return list(sum(_list,()))

# OPERATION AT STRINGS
def is_verb(word = None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')
# FILTER FOR ARRAYS
def is_none_filter(array):
    node_list = [map(is_astFunction_instance_filter(y), ast.walk(y)) for y in array]
    return filter(None, node_list) # OPTIMIZE <---------------------- need to delete somehow
# FILTERING
def filter_only_py_extention(file, from_path):
    if file.endswith('.py'):
        return os.path.join(from_path, file)
# SEARCHING
def find_py_files(from_path = Path):
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown = True):
        # files_list = [ filter_only_py_extention(file, whole_path) for file in files ] #if len(files_list) != 100 ]        
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
    # FIX no clearly stated conditions 
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

def get_common_verbs_across(path, projects):
    words = []
    for project in projects:
        # path = os.path.join('.', project)
        words.append(cascade_call(path))
    print('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in the_most_common(words):
        print(word, occurence)

# UNUSED
# 
# def get_all_names(tree):
#     return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
#
# def split_snake_case_name_to_words(name):
#     return [n for n in name.split('_') if n]
#     return flattening([split_snake_case_name_to_words(function_name) for function_name in function_names])

# def get_top_functions_names_in_path(path, top_size=10):
#     t = get_trees(path)
#     nms = [f for f in flattening([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.Functi
# onDef)] for t in t]) if not (f.startswith('__') and f.endswith('__'))]
#     return collections.Counter(nms).most_common(top_size)


# UNNESSESARY
# def flatten(array):
#     return [arr for arr in flattening(array)]

