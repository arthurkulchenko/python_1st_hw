from nltk import pos_tag, word_tokenize
from support_methods import *

def stringify(not_a_string):
    return "%s" % not_a_string


def determine_part_of_speech(_word_, required_part_of_speech):
    word = getting_rid_of_underscore_in(_word_)
    tagged_word = pos_tag(word_tokenize(word))
    if required_part_of_speech == 'verb':
        if tagged_word[0][1] in ('VB', 'VBD', 'VBZ', 'VBN'):
            return word
    elif required_part_of_speech == 'noun':
        if tagged_word[0][1] == ('NN'):
            return word
    else:
        return 'Rather verb or noun'

# NOTICE
def getting_rid_of_underscore_in(_word_):
    result = re.split("[\_]+", _word_)
    return filter(None, result)[0]


def split_snake_case_names_into_words(from_list):
    nested_array = [i.split('_') for i in from_list if (type(i) is not 'bool')]
    return list(flattening(nested_array))
