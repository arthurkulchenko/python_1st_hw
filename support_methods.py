import os
import re
import ast
import git
import csv
import json
import collections
import logging
from nltk import pos_tag, word_tokenize
from constants import FILES_AMOUNT


def flattening(l):
    for e in l:
        if isinstance(e, collections.Iterable) and not isinstance(e, basestring):
            for sub in flattening(e):
                yield sub
        else:
            yield e


def extention_only(file, from_path, extention):
    if file is not None and file.endswith(extention):
        return os.path.join(from_path, file)


def the_most_common_of(objects, top_size=FILES_AMOUNT):
    return collections.Counter(objects).most_common(top_size)


def get_current_dir_path(path_with_file=os.path.realpath(__file__)):
    exclusion_regex = "[\/][\w]+['.'][\D]+"
    dir_path = re.split(exclusion_regex, path_with_file)[0]
    return dir_path


def ast_file_parser(file):
    with open(file, 'r') as file_viewer:
        file_content = file_viewer.read()
    try:
        return ast.parse(file_content)
    except SyntaxError as e:
        logging.error(e)
        return None


def variables_names(nodes):
    ast_name_nodes = map(is_astName_filter, nodes)
    ast_name_nodes = filter(None, ast_name_nodes)
    variables = [node.id for node in ast_name_nodes]
    splitted = split_snake_case_names_into_words(variables)
    variables = filter(None, splitted)
    return variables


def is_astName_filter(a):
    if isinstance(a, ast.Name):
        return a


def is_astFDef_filter(a):
    if isinstance(a, ast.FunctionDef):
        return a


def functions_names(nodes):
    ast_fdef_nodes = map(is_astFDef_filter, nodes)
    ast_fdef_nodes = filter(None, ast_fdef_nodes)
    function_names = [node.name for node in ast_fdef_nodes]
    splitted = split_snake_case_names_into_words(function_names)
    function_names = filter(None, splitted)
    return function_names


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


def location_determining(source, path):
    if source is not 'none':
        location = git_clone(source, path)
    else:
        location = path
    return location


def output_method(data_format, data):
    if data_format == 'json':
        with open('result.json', 'w') as json_file:
            json.dump(data, json_file)
    elif data_format == 'csv':
        with open('result.csv', 'wb') as csv_file:
            csv_result = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            csv_result.writerow(data)
    else:
        logging.info(data)


def search_in(list, required_part_of_speech):
    extracted = [word_extraction(i, required_part_of_speech) for i in list]
    return filter(None, extracted)


def word_extraction(word, required_part_of_speech):
    tagged_word = pos_tag(word_tokenize(word))
    if required_part_of_speech in ('verb', 'verbs'):
        if tagged_word[0][1] in ('VB', 'VBD', 'VBZ', 'VBN', 'VBG'):
            return word
    elif required_part_of_speech in ('noun', 'nouns'):
        if tagged_word[0][1] == ('NN'):
            return word
    else:
        return 'None'


def split_snake_case_names_into_words(from_list):
    nested_array = [i.split('_') for i in from_list if (type(i) is not 'bool')]
    return list(flattening(nested_array))
