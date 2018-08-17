import os
import ast
import logging
from constants import FILES_AMOUNT
import argument_parser
from support_methods import *

logging.basicConfig(level=logging.INFO)


def find_files_by_extention(from_path, extention, amount):
    files_list = []
    for whole_path, dirs, files in os.walk(from_path, topdown=True):
        for file in files:
            files_list.append(extention_only(file, whole_path, extention))
            if len(files_list) >= amount:
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


def run(args=argument_parser.args):
    location = location_determining(args.source, args.path)
    files = find_files_by_extention(location, args.extention, args.amount)
    if args.entities == 'functions':
        entity = node_names(get_trees(files))
    else:
        entity = variables_names(get_trees(files))
    logging.info('Looking in %s' % args.entities)
    if args.part_of_speech == 'verbs':
        result = search_for_verbs(entity)
    else:
        result = search_for_noun(entity)
    logging.info('Looking for %s' % args.part_of_speech)
    semi_result = the_most_common_of(entity, len(result))
    dictionary = dict((x,y) for x, y in semi_result)
    output_method(args.output, dictionary)
