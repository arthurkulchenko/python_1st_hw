import os
import ast
import sys
import csv
import json
import logging
from itertools import izip
import argument_parser
from support_methods import *

logging.basicConfig(level=logging.INFO)


def __test_method__():
    pass


def find_files_by_extention(from_path, extention):
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown=True):
        for file in files:
            files_list.append(extention_only(file, whole_path, extention))
            if len(files_list) >= 100:
                break
    files_list = filter(None, files_list)
    logging.info('Total found *.%s files amount is: %s' % (extention, len(files_list)))
    return files_list


def get_trees(files):
    trees = []
    for file in files:
        with open(file, 'r') as file_viewer:
            file_content = file_viewer.read()
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            logging.error("%s in get_trees method." % e)
            tree = None
        trees.append(tree)
    trees = filter(None, trees)
    logging.info('trees generated')
    return trees


# NOTICE DEPRICATED
def get_common_verbs(trees):
    flatten_array = flattening(only_astF_instances(trees))
    functions_list = [stringify(is_private(f)) for f in flatten_array]
    functions_list = filter(None, functions_list)
    logging.info('functions extracted')
    g = [getting_verbs(function_name) for function_name in functions_list]
    return list(flattening(g))


# NOTICE DEPRICATED
def cascade_call(path):
    py_files = find_files_by_extention(path)
    trees = get_trees(py_files)
    result = get_common_verbs(trees)
    logging.info(result)
    return result


# NOTICE DEPRICATED
def get_common_verbs_across(projects):
    words = []
    for project in projects:
        path = os.path.join('.', project)
        words.append(cascade_call(path))
    logging.info('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in the_most_common(words):
        logging.info(word, occurence)


# NOTICE DEPRICATED
def cascade():
    py_files = find_files_by_extention()
    trees = get_trees(py_files)
    verbs = get_common_verbs(trees)
    logging.info(the_most_common_of(verbs))
    return the_most_common_of(verbs)


# NOTICE DEPRICATED
def switch_case_2(element):
    dictionary = {
        "-c": "cascade()",
        "-h": "help_dialog()"
    }
    return dictionary.get(stringify(element))


def run(args=argument_parser.args):
    if args.source is not 'none':
        location = git_clone(args.source, args.path)
        logging.info('Repo downloaded to: '+location)
    else:
        location = args.path
    files = find_files_by_extention(location, args.extention)
    if args.entities == 'functions':
        logging.info('Looking in functions')
        entity = node_names(get_trees(files))
        print entity
    else:
        entity = variables_names(get_trees(files))
        print entity
        logging.info('Looking in variables')
    if args.part_of_speech == 'verbs':
        
        result = search_verbs(entity)
        print entity
        logging.info('Looking for verbs')
    else:
        result = search_noun(entity)
        print entity
        logging.info('Looking for noun')
    entity = result
    result = the_most_common_of(entity, len(entity))
    dictionary = dict((x,y) for x, y in result)
    if args.output == 'json':
        with open('result.json', 'w') as json_file:
            json_result = json.dump(dictionary, json_file)
    elif args.output == 'csv':
        with open('result.csv', 'wb') as csv_file:
            csv_result = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            csv_result.writerow(result)


# NOTICE DEPRICATED
def help_dialog():
    print '''
            Hello I am a helper \n\n 
        -h :call this helper \n
        -c :call the most common verbs in *py files'''
