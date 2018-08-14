
import os
import argparse
# from code_observer import *
from support_methods import *

parser = argparse.ArgumentParser(description='''
	This proram can help you to count words in your file or in banch of files.\n\n
	Please provide path to any (or only *py in this realization) directory.
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
					help=':choose output console, json, csv'
					)

parser.add_argument(
					'-s',
					dest='source',
					action='store',
					default='none',
					help=':clone external repo "default: github"'
					)

parser.add_argument(
					'-w',
					dest='words',
					action='store',
					default='functions',
					help=':search for the most common words in functions or variables names'
					)

parser.add_argument(
					'-v',
					dest='verbs',
					action='store',
					default='functions',
					help=':statistic about amount of VERBS in functions or variables names'
					)

parser.add_argument(
					'-n',
					dest='noun',
					action='store',
					default='functions',
					help=':statistic about amount of NOUN in functions or variables names'
					)

args = parser.parse_args()
