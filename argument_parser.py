import argparse
from support_methods import get_current_dir_path
from constants import FILES_AMOUNT

parser = argparse.ArgumentParser(description='''
    This proram can help you to count words in your file or in
    banch of files.\n\n
    Please provide path to any (or only *py in this realization) directory or
    just leave it blank to scan current directory.
''')

parser.add_argument(
                    '-p',
                    dest='path',
                    action='store',
                    default=get_current_dir_path(),
                    help=':path to the directory (default: current direcrory)'
                   )


parser.add_argument(
                    '-e',
                    dest='extention',
                    action='store',
                    default='py',
                    help=':file type (default: *.py)'
                   )


parser.add_argument(
                    '-o',
                    dest='output',
                    action='store',
                    default='console',
                    help=':choose output method console, json, csv'
                   )


parser.add_argument(
                    '-s',
                    dest='source',
                    action='store',
                    default='none',
                    help=':clone external repo "default: github"'
                   )


parser.add_argument(
                    '-en',
                    dest='entities',
                    action='store',
                    default='functions',
                    help='''
                    :search for the most common words
                    in functions or variables names'''
                   )


parser.add_argument(
                    '-ps',
                    dest='part_of_speech',
                    action='store',
                    default='verbs',
                    help='''
                    :statistic about amount of VERBS and NOUNS
                    in functions and variables names, default: verbs'''
                   )


parser.add_argument(
                    '-a',
                    dest='amount',
                    action='store',
                    default=FILES_AMOUNT,
                    help=':max of observation list files, default: 100'
                   )


args = parser.parse_args()
