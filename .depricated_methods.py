
def args_handler(arguments):
    args = []
    args.append(arguments)
    args = filter(None, args)
    return list(flattening(args))


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


def get_common_verbs(trees):
    flatten_array = flattening(only_astF_instances(trees))
    functions_list = [stringify(is_private(f)) for f in flatten_array]
    functions_list = filter(None, functions_list)
    logging.info('functions extracted')
    g = [getting_verbs(function_name) for function_name in functions_list]
    return list(flattening(g))


def cascade_call(path):
    py_files = find_files_by_extention(path)
    trees = get_trees(py_files)
    result = get_common_verbs(trees)
    logging.info(result)
    return result


def get_common_verbs_across(projects):
    words = []
    for project in projects:
        path = os.path.join('.', project)
        words.append(cascade_call(path))
    logging.info('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in the_most_common(words):
        logging.info(word, occurence)


def cascade():
    py_files = find_files_by_extention()
    trees = get_trees(py_files)
    verbs = get_common_verbs(trees)
    logging.info(the_most_common_of(verbs))
    return the_most_common_of(verbs)


def switch_case_2(element):
    dictionary = {
        "-c": "cascade()",
        "-h": "help_dialog()"
    }
    return dictionary.get(stringify(element))


def help_dialog():
    print '''
            Hello I am a helper \n\n 
        -h :call this helper \n
        -c :call the most common verbs in *py files'''


def is_verb(word=None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')


def is_noun(word=None):
    print word
    if word == (None or "" or " "):
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        if pos_info[0][1] == ('NN'):
            return word


def search_for_verbs(array):
    list = [is_verb(i) for i in array]
    list = filter(None, list)
    return split_snake_case(list)


def search_for_noun(array):
    words = split_snake_case(array)
    list = [is_noun(i) for i in words]
    list = filter(None, list)
    return list


def getting_verbs(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]
