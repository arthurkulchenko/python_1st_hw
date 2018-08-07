import sys
import os
import ast
import re
import collections
from constants import *
from nltk import pos_tag, word_tokenize
""", punkt"""


def flattening(l):
    for e in l:
        if isinstance(e, collections.Iterable) and not isinstance(e, basestring):
            for sub in flattening(e):
                yield sub
        else:
            yield e


def is_verb(word=None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')


def only_astF_instances(array):
    node_list = [map(is_astF_instance_filter(y), ast.walk(y)) for y in array]
    return filter(None, node_list)


def filter_only_py(file, from_path):
    return os.path.join(from_path, extention_filter(file))


def extention_filter(file, extention='.py'):
    if file.endswith(extention):
        return file


def the_most_common_of(objects, top_size=10):
    return collections.Counter(objects).most_common(top_size)


def is_astF_instance_filter(node):
    if isinstance(node, ast.FunctionDef):
        return node.name.lower()


def getting_verbs(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def is_private(thing):
    if type(thing).__name__.startswith('__'):
        if type(thing).__name__.endswith('__'):
            return type(thing).__name__


def stringify(not_a_string):
    return "%s" % not_a_string


def getting_file_path(path_with_file):
    exclusion_regex = "[\/][\w]+['.'][\D]+"
    dir_path = re.split(exclusion_regex, path_with_file)[0]
    return dir_path


def path_setter(path=sys.argv):
    global PATH
    PATH = getting_file_path(os.path.realpath(__file__))
    print PATH
    args = []
    args.append(path)
    args = filter(None, args)
    args = list(flattening(args))
    if len(args) >= 3:
        if args[1] == '-d':
            PATH = args[2]
    else:
        inputed_value = raw_input('''You didn\'t provide working directory,
                                     may I offer current directory?: y/n?\n''')
        if inputed_value == 'y':
            PATH = getting_file_path(os.path.realpath(__file__))
        else:
            inputed_value = raw_input('Please type in the path: \n')
            PATH = inputed_value
    return PATH
