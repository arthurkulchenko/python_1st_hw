import os
import ast
import logging
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
    list = filter(None, files_list)
    logging.info('Found %s *.%s files' % (len(list), extention))
    return list


def get_nodes(files):
    trees = filter(None, map(ast_file_parser, files))
    return list(flattening([ast.walk(t) for t in trees]))


def run(args=argument_parser.args):
    location = location_determining(args.source, args.path)
    files = find_files_by_extention(location, args.extention, args.amount)
    if args.entities == 'functions':
        entity_list = functions_names(get_nodes(files))
    else:
        entity_list = variables_names(get_nodes(files))
    logging.info('Searching in %s...' % args.entities)
    words = search_in(entity_list, args.part_of_speech)
    logging.info('Looking for %s' % args.part_of_speech)
    semi_result = the_most_common_of(words, len(words))
    dictionary = dict((x, y) for x, y in semi_result)
    output_method(args.output, dictionary)
