if __name__ == "constants":


	PATH = ''
	TOP_SIZE = 200
	PROJECTS = [
                	'django',
                	'flask',
                	'pyramid',
                	'reddit',
                	'requests',
                	'sqlalchemy',
            	]


def path_setter():
	if PATH == '':
		PATH = input('Enter please directory path: ')
		