import os
import re
import ast
import git
import sys
import collections
from lang_work import *


def flattening(l):
    for e in l:
        if isinstance(e, collections.Iterable) and not isinstance(e, basestring):
            for sub in flattening(e):
                yield sub
        else:
            yield e


def only_astF_instances(array):
    node_list = [map(is_astF_instance_filter(y), ast.walk(y)) for y in array]
    return filter(None, node_list)


def extention_only(file, from_path, extention):
    if file != None and file.endswith(extention):
        return os.path.join(from_path, file)


def the_most_common_of(objects, top_size=100):
    return collections.Counter(objects).most_common(top_size)


def is_astF_instance_filter(node):
    if isinstance(node, ast.FunctionDef):
        return node.name.lower()


def is_private(thing):
    if not type(thing).__name__.startswith('__'):
        return type(thing).__name__
        # if not type(thing).__name__.endswith('__'):


def get_current_dir_path(path_with_file=os.path.realpath(__file__)):
    exclusion_regex = "[\/][\w]+['.'][\D]+"
    dir_path = re.split(exclusion_regex, path_with_file)[0]
    return dir_path


# NOTICE DEPRICATED
def args_handler(arguments):
    args = []
    args.append(arguments)
    args = filter(None, args)
    return list(flattening(args))


# NOTICE DEPRICATED
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


def variables_names(trees):
    n = []
    for t in trees:
        n.append([node.id for node in ast.walk(t) if isinstance(node, ast.Name)])
    variables = list(flattening(n))
    variables = filter(None, variables)
    return variables


def git_clone(repo, destination, required_branch='master'):
    repo_name_re = re.search("[\w]+['.'][git]+", repo).group(0)
    folder_name = re.split("[.][\w]+", repo_name_re)[0]
    location = destination+'/'+folder_name+'/'+required_branch
    git.Repo.clone_from(
                        repo,
                        location,
                        branch=required_branch
                        )
    logging.info('Repo downloaded to: '+location)
    return location


def node_names(array):
    flat_array = flattening([list(ast.walk(y)) for y in array])
    return [node.__class__.__name__ for node in flat_array]


# def to_json(object):
#     obj = dict((x,y) for x, y in object)
#     json_result = json.dumps(obj, outfile)
#     loaded_json = json.loads(json_result)
