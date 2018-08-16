import os
import re
import ast
import git
import sys
import csv
import json
import collections
from lang_work import *
from constants import FILES_AMOUNT


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


def the_most_common_of(objects, top_size=FILES_AMOUNT):
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


def location_determining(source, path):
    if source is not 'none':
        location = git_clone(source, path)
    else:
        location = path
    return location


def output_method(data_format, data):
    if data_format == 'json':
        with open('result.json', 'w') as json_file:
            json_result = json.dump(data, json_file)
    elif data_format == 'csv':
        with open('result.csv', 'wb') as csv_file:
            csv_result = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            csv_result.writerow(result)
    else:
        logging.info(data)
