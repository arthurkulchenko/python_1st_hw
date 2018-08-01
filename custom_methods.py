import os
import ast
import collections
from nltk import pos_tag, word_tokenize
""", punkt"""


def flattening(l):
    if type(l) == 'List':
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in flattening(el):
                    yield sub
            else:
                yield el
    else:
        return list(sum(l, ()))


def is_verb(word=None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')


def is_none_filter(array):
    node_list = [map(is_astF_instance(y), ast.walk(y)) for y in array]
    return filter(None, node_list)


def filter_only_py_extention(file, from_path):
    if file.endswith('.py'):
        print file
        return os.path.join(from_path, file)


def the_most_common(objects, top_size=10):
    return collections.Counter(objects).most_common(top_size)


def is_astF_instance(node):
    if isinstance(node, ast.FunctionDef):
        return node.name.lower()
