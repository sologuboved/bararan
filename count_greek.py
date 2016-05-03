# -*- coding: utf-8 -*-

import json

TRANSLATION = 'translation'
ARTICLE = 'article'
WORD = 'word'
CATEGORIES = 'categories'
INSTALLMENT = 'installment'
EXAMPLE = 'example'
GRAMMAR = 'grammar'
MISC = 'misc'
JSON_FILE = 'json_lexilogio.json'

FIELDS = {TRANSLATION, ARTICLE, WORD, CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, MISC}

def load_json(json_file):
    with open(json_file) as data:
        dictionary = json.load(data)
        return dictionary

def count_words(dictionary):
    return len(dictionary)


def count_words_by_cat(dictionary):
    categories = dict()
    for entry in dictionary:
        if dictionary[entry].get(CATEGORIES):
            for cat in dictionary[entry][CATEGORIES]:
                if cat not in categories:
                    categories[cat] = 1
                else:
                    categories[cat] += 1
    return categories


def print_count_by_cat(categories_dict):
    for cat in categories_dict:
        print cat + ': ' + unicode(categories_dict[cat])


def count_duplicates(dictionary):
    words = dict()
    for id in dictionary:
        if dictionary[id][WORD] not in words:
            words[dictionary[id][WORD]] = 1
        else:
            words[dictionary[id][WORD]] += 1
    print len(words)
    duplicates = dict()
    for word in words:
        if words[word] > 1:
            print word, words[word]
            duplicates[word] = words[word]
    print len(duplicates)
    print duplicates


if __name__ == '__main__':
    my_dict = load_json(JSON_FILE)
    # print 'total words', count_words(my_dict)
    print
    # cats = count_words_by_cat(my_dict)
    # print_count_by_cat(cats)
    count_duplicates(my_dict)

