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
FIELDS = [WORD, ARTICLE, TRANSLATION,  CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, MISC]


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


def add_categories(dictionary, index):
    while index < len(dictionary):
        entry_id = unicode(index)
        current_entry = dictionary[entry_id]
        print entry_id + ')' + ' ' + current_entry[WORD] + ' ' + '(' + current_entry[TRANSLATION][0] + '):'
        for category in current_entry[CATEGORIES]:
            print category
        new_categories = raw_input("Input new Categories, space separated, or 'b' for break: ").split()
        if new_categories and new_categories[0] == 'b':
            break
        dictionary[entry_id][CATEGORIES].extend(new_categories)
        current_entry = dictionary[entry_id]
        print 'Now:', entry_id + ')', current_entry[WORD] + ':'
        for category in current_entry[CATEGORIES]:
            print category
        index += 1
    return index, dictionary


def launch_category_adder(json_file, index):
    old_dictionary = load_json(json_file)
    stopped_at, new_dictionary = add_categories(old_dictionary, index)
    dump_json(new_dictionary, json_file)
    print
    print "Stopped at", stopped_at


def is_correct_type(field, modification):
    if field not in FIELDS:
        return False
    if (field == WORD or field == INSTALLMENT) and type(modification) != str:
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


def rename_category(dictionary, old_name, new_name):
    count = 0
    for entry_id in dictionary:
        entry = dictionary[entry_id]
        categories = entry[CATEGORIES]
        if old_name in categories:
            categories.remove(old_name)
            categories.append(new_name)
            count += 1
    return count, dictionary


def launch_category_renamer(json_file, old_name, new_name):
    old_name = unicode(old_name, 'utf-8')
    old_dictionary = load_json(json_file)
    count, new_dictionary = rename_category(old_dictionary, old_name, new_name)
    dump_json(new_dictionary, json_file)
    print old_name, "changed to", new_name, count, "time(s)"


def pretty_print(dictionary, start, end=None):
    length = len(dictionary)
    assert start < length, "Start %d not in range [0, %d)" % (start, length)
    if end:
        assert start < end < length, "End %d not in range (%d, %d)" % (end, start, length)
        while start < end:
            print_entry(dictionary, start)
            start += 1
    else:
        print_entry(dictionary, start)


def print_entry(dictionary, index):
    entry_id = unicode(index)
    entry = dictionary[entry_id]
    print entry_id
    for field in FIELDS:
        print_field(entry, field)
    print


def print_field(entry, field):
    subentry = entry[field]
    if type(subentry) == list:
        print field + ':'
        for item in subentry:
            print '    ' + item
    else:
        print field + ':', subentry


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
    # launch_category_adder(JSON_FILE, 0)
    launch_category_renamer(JSON_FILE, 'ουσιαστικό', 'ουσιαστικά')
    my_dict = load_json(JSON_FILE)
    pretty_print(my_dict, 0, 10)
