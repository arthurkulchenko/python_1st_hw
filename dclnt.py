import ast
import os
import collections
from nltk import pos_tag, word_tokenize, punkt

PATH = ''
TOP_SIZE = 200
PROJECTS = [
                'django',
                'flask',
                'pyramid',
                'reddit',
                'requests',
                'sqlalchemy',
            ]
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
# # OPERATION AT TUPLES
# def flattening(_list):
#     return list(sum(_list,()))
# OPERATION AT STRINGS
def is_verb(word = None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')
# FILTERING
def filter_only_py_extention(file, from_path):
    if file.endswith('.py'):
        return os.path.join(from_path, file)
# SEARCHING
def find_py_files(from_path = Path):
    py_files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown = True):
        # OPTIMIZE py_files_list = [ filter_only_py_extention(each_file, whole_path) for each_file in files if len(py_files_list) <= 100 ]
        for file in files:
            py_files_list.append(filter_only_py_extention(file, whole_path))
            if len(py_files_list) >= 100:
                break
    py_files_list = filter(None, py_files_list)
    print('Total finded *.py files amount is: %s' % len(py_files_list))
    return py_files_list
# SEARCHING
def get_trees(with_files = False, with_file_content = False):
    files = find_py_files()
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
# FILTER CHECKING IS A METHOT IS PRIVATE
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
# FILTER FOR ARRAYS
def is_none_filter(array):
    node_list = [map(is_astFunction_instance_filter(y), ast.walk(y)) for y in array]
    return filter(None, node_list) # OPTIMIZE <---------------------- need to delete somehow
# should be called from get_common_verbs_across
def get_common_verbs():
    flatten_array = flattening(is_none_filter(get_trees()))
    fncs = [is_private_filter_and_stringify(f) for f in flatten_array]
    fncs = filter(None, fncs)
    print('functions extracted')
    return flattening([get_verbs_from_function_name(function_name) for function_name in fncs])

# SCOPE METHOD 
def the_most_common(objects, top_size=10):
    return collections.Counter(objects).most_common(top_size)

def get_common_verbs_across(projects, path):
    # words = []
    # for project in projects:
    #     path = os.path.join('.', project)
    #     words += get_common_verbs(path)
    words = [ get_common_verbs() for words in projects]

    print('total %s words, %s unique' % (len(words), len(set(words))))
    # for word, occurence in collections.Counter(words).most_common(top_size):
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
#     nms = [f for f in flattening([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]) if not (f.startswith('__') and f.endswith('__'))]
#     return collections.Counter(nms).most_common(top_size)


# UNNESSESARY
# def flatten(array):
#     return [arr for arr in flattening(array)]

