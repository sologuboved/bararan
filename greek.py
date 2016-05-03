# -*- coding: utf-8 -*-

import csv
import json

TRANSLATION = 'translation'
ARTICLE = 'article'
WORD = 'word'
CATEGORIES = 'categories'
INSTALLMENT = 'installment'
EXAMPLE = 'example'
GRAMMAR = 'grammar'
MISC = 'misc'
CSV_FILE = 'greek_words.csv'
JSON_FILE = 'json_lexilogio.json'
JSON_FILE_COPY = 'json_lexilogio_copy.json'

FIELDS = {TRANSLATION, ARTICLE, WORD, CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, MISC}


def make_dict(csv_file):
    dictionary = dict()
    index = 0
    with open(csv_file) as f:
        wordreader = csv.reader(f)
        for row in wordreader:
            dictionary[index] = {TRANSLATION: [row[0]],
                                 ARTICLE: [row[1]],
                                 WORD: row[2],
                                 CATEGORIES: [row[3]],
                                 INSTALLMENT: row[4],
                                 EXAMPLE: list(),
                                 GRAMMAR: list(),
                                 MISC: list()}
            index += 1
    return dictionary


def dump_json(dictionary, fname):
    with open(fname, 'w') as fp:
        json.dump(dictionary, fp)


def load_json(json_file):
    with open(json_file) as data:
        dictionary = json.load(data)
        return dictionary


def add_categories(json_file, index):
    dictionary = load_json(json_file)
    while index < len(dictionary):
        key = unicode(index)
        current_entry = dictionary[key]
        print key + ')' + ' ' + current_entry[WORD] + ' ' + '(' + current_entry[TRANSLATION][0] + '):'
        for category in current_entry[CATEGORIES]:
            print category
        new_categories = raw_input("Input new Categories, space separated, or 'b' for break: ").split()
        if new_categories and new_categories[0] == 'b':
            break
        dictionary[key][CATEGORIES].extend(new_categories)
        current_entry = dictionary[key]
        print key + ')', current_entry[WORD] + ':'
        for category in current_entry[CATEGORIES]:
            print category
        index += 1
    return index, dictionary


def launch_category_adder(json_file, index):
    stopped_at, words = add_categories(json_file, index)
    print
    print "Stopped at", stopped_at
    dump_json(words, json_file)


def is_correct_type(field, modification):
    if field not in FIELDS:
        return False
    if (field == WORD or field == INSTALLMENT) and type(modification) != unicode:
        return False
    if type(modification) != list:
        return False
    return True


def get_proper_id(dictionary, some_id):
    pass


def make_corrections(json_file, some_id, field, correction):
    if not is_correct_type(field, correction):
        print correction, "does not go into", field
        return
    dictionary = load_json(json_file)
    try:
        some_id = unicode(int(some_id))
        entry = dictionary.get(some_id)
    except ValueError:
        for key in dictionary:
            if dictionary[key][WORD] == some_id:
                entry = dictionary[key]
                break
        else:
            entry = None
    if entry:
        pass



def rename_category(json_file, some_id):
    pass


def test_json_maker(test_json_file):
    words = make_dict(CSV_FILE)
    # curr = 0
    # while curr < 10:
    #     print words[curr][TRANSLATION][0], words[curr][WORD], words[curr][CATEGORIES][0], words[curr][INSTALLMENT]
    #     curr += 1
    dump_json(words, test_json_file)
    dictionary = load_json(test_json_file)
    index = 0
    while index < 10:
        key = unicode(index)
        current_entry = dictionary[key]
        intro = key + ')', current_entry[WORD], '(' + current_entry[TRANSLATION][0] + '):'
        print
        try:
            print intro, current_entry[CATEGORIES][0]
        except IndexError:
            print intro, current_entry[CATEGORIES]
        index += 1


if __name__ == '__main__':
    # test_json_maker('test.json')
    # launch_category_adder(0)
    # make_json(make_dict(CSV_FILE), JSON_FILE)
    launch_category_adder(JSON_FILE, 0)
