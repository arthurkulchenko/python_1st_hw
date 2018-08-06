import os
import ast
import collections
from nltk import pos_tag, word_tokenize
""", punkt"""


def flattening(l):
    if type(l) == 'List':
        for e in l:
            if isinstance(e, collections.Iterable) and not isinstance(e, basestring):
                for sub in flattening(e):
                    yield sub
            else:
                yield e
    else:
        return list(sum(l, ()))


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
            return thing.__class__.__name__


def stringify(not_a_string):
    return "%s" % not_a_string
