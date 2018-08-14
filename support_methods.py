import os
import re
import ast
import git
import sys
import collections
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


def extention_only(file, from_path, extention):
    if file != None and file.endswith(extention):
        return os.path.join(from_path, file)


def the_most_common_of(objects, top_size=10):
    return collections.Counter(objects).most_common(top_size)


def is_astF_instance_filter(node):
    if isinstance(node, ast.FunctionDef):
        return node.name.lower()


def getting_verbs(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def is_private(thing):
    if not type(thing).__name__.startswith('__'):
        if not type(thing).__name__.endswith('__'):
            return type(thing).__name__


def stringify(not_a_string):
    return "%s" % not_a_string


def get_current_dir_path(path_with_file=os.path.realpath(__file__)):
    exclusion_regex = "[\/][\w]+['.'][\D]+"
    dir_path = re.split(exclusion_regex, path_with_file)[0]
    return dir_path


#NOTICE DEPRICATED
def args_handler(arguments):
    args = []
    args.append(arguments)
    args = filter(None, args)
    return list(flattening(args))


#NOTICE DEPRICATED
def path_setter(path=sys.argv):
    global PATH
    PATH = get_current_dir_path(os.path.realpath(__file__))
    args = args_handler(path)
    if len(args) >= 3:
        if args[1] == '-d':
            PATH = args[2]
    else:
        inputed_value = raw_input('''
            You didn\'t specify the directory you want
            to scan, may I offer current directory?: y/n?\n''')
        if inputed_value == 'y':
            PATH = get_current_dir_path(os.path.realpath(__file__))
        else:
            inputed_value = raw_input('Please type in the path: \n')
            PATH = inputed_value
    return PATH


def get_all_names(trees):
    for t in trees:
        n = [node.id for node in ast.walk(t) if isinstance(node, ast.Name)]
    return filter(None, n)


def split_snake_case_names_into_words(from_list):
    nested_array = [i.split('_') for i in from_list]
    return list(flattening(nested_array))


def git_clone(repo, destination, required_branch='master'):
    repo_name_re = re.search("[\w]+['.'][git]+", repo).group(0)
    folder_name = re.split("[.][\w]+", repo_name_re)[0]
    git.Repo.clone_from(
                        repo,
                        destination+'/'+folder_name+'/'+required_branch,
                        branch=required_branch
                        )
    return destination+'/'+folder_name+'/'+required_branch
