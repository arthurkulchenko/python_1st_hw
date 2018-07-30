import ast
import os
import collections
from nltk import pos_tag, word_tokenize, punkt

Path = ''

def flattening(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flattening(el):
                yield sub
        else:
            yield el

def flatten(array):
    return [arr for arr in flattening(array)]

def flattening_tuple(_list):
    return list(sum(_list,()))

def is_verb(word = None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')

def only_py_extention(file, from_path):
    if file.endswith('.py'):
        return os.path.join(from_path, file)

def find_py_files(from_path = Path):
    py_files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown = True):
        for each_file in files:
            py_files_list.append(only_py_extention(each_file, whole_path))
            if len(py_files_list) == 100:
                break
    py_files_list = filter(None, py_files_list)
    print('Total finded *.py files amount is: %s' % len(py_files_list))
    return py_files_list

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
    return filter(None, node_list)
# SCOPE METHOD 
def get_top_verbs_in_path(top_size=10):
    flatten_arr = flatten(is_none_filter(get_trees()))
    fncs = [is_private_filter_and_stringify(f) for f in flatten_arr]
    fncs = filter(None, fncs)
    print('functions extracted')
    verbs = flattening([get_verbs_from_function_name(function_name) for function_name in fncs])
    return collections.Counter(verbs).most_common(top_size)

def some_wierd_stuff():
    wds = []
    projects = [
                'django',
                'flask',
                'pyramid',
                'reddit',
                'requests',
                'sqlalchemy',
                ]

    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)

top_size = 200
print('total %s words, %s unique' % (len(wds), len(set(wds))))
for word, occurence in collections.Counter(wds).most_common(top_size):
    print(word, occurence)

# UNUSED
# 
# def get_all_names(tree):
#     return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
#
# def split_snake_case_name_to_words(name):
#     return [n for n in name.split('_') if n]
#     return flattening_tuple([split_snake_case_name_to_words(function_name) for function_name in function_names])

# def get_top_functions_names_in_path(path, top_size=10):
#     t = get_trees(path)
#     nms = [f for f in flattening_tuple([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]) if not (f.startswith('__') and f.endswith('__'))]
#     return collections.Counter(nms).most_common(top_size)

