import ast
import os
import collections

from nltk import pos_tag, word_tokenize, punkt

def flat(_list):
    return list(sum(_list,()))

def is_verb(word = None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')

Path = ''

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

def get_trees(_path, with_filenames = False, with_file_content = False):
    filenames = find_py_files()
    trees = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    trees = [t for t in get_trees(path) if t]
    function_names = [f for f in flat([get_all_names(t) for t in trees]) if not (f.startswith('__') and f.endswith('__'))]
    def split_snake_case_name_to_words(name):
        return [n for n in name.split('_') if n]
    return flat([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_top_verbs_in_path(path, top_size=10):
    global Path
    Path = path
    trees = [t for t in get_trees(None) if t]
    fncs = [f for f in flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees]) if not (f.startswith('__') and f.endswith('__'))]
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in fncs])
    return collections.Counter(verbs).most_common(top_size)
def get_top_functions_names_in_path(path, top_size=10):
    t = get_trees(path)
    nms = [f for f in flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]) if not (f.startswith('__') and f.endswith('__'))]
    return collections.Counter(nms).most_common(top_size)


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


