from nltk import pos_tag, word_tokenize
""", punkt"""
from support_methods import *

def stringify(not_a_string):
    return "%s" % not_a_string


def is_verb(word=None):
    if word is None:
        return False
    else:
        pos_info = pos_tag(word_tokenize(word))
        return pos_info[0][1] in ('VB', 'VBD', 'VBZ', 'VBN')


def is_noun(word=None):
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


def getting_rid_of_underscore_in(_word_):
    result = re.split("[\_]+", _word_)
    return filter(None, result)[0]


def split_snake_case(from_list):
    nested_array = [stringify(i).split('_') for i in from_list if (type(i) is not 'bool')]
    return list(flattening(nested_array))


def split_snake_case_names_into_words(from_list):
    nested_array = [i.split('_') for i in from_list if (type(i) is not 'bool')]
    return list(flattening(nested_array))


def getting_verbs(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]
