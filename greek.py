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
        print
        index += 1
    return index


def launch_category_adder(json_file, index):
    dictionary = load_json(json_file)
    stopped_at = add_categories(dictionary, index)
    dump_json(dictionary, json_file)
    print "Stopped at", stopped_at


def is_correct_type(field, modification):
    if field not in FIELDS:
        return False
    if (field == WORD or field == INSTALLMENT) and type(modification) != str:
        return False
    if type(modification) != list:
        return False
    return True


def get_actual_id(dictionary, some_id):
    actual_id = None
    try:
        some_id = unicode(int(some_id))
        if some_id in dictionary:
            actual_id = some_id
    except ValueError:
        some_id = unicode(some_id, 'utf-8')
        for entry_id in dictionary:
            if dictionary[entry_id][WORD] == some_id:
                actual_id = entry_id
                break
    return actual_id


def make_corrections(json_file, some_id, field, correction):
    # TODO unfinished
    if not is_correct_type(field, correction):
        print correction, "does not go into", field
        return


def rename_category(dictionary, old_name, new_name):
    count = 0
    for entry_id in dictionary:
        entry = dictionary[entry_id]
        categories = entry[CATEGORIES]
        if old_name in categories:
            categories.remove(old_name)
            categories.append(new_name)
            count += 1
    return count


def launch_category_renamer(json_file, old_name, new_name):
    old_name = unicode(old_name, 'utf-8')
    dictionary = load_json(json_file)
    count = rename_category(dictionary, old_name, new_name)
    dump_json(dictionary, json_file)
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


def launch_json_maker(csv_file, json_file):
    dictionary = make_dict(csv_file)
    index = 0
    while index < 10:
        print dictionary[index][TRANSLATION][0], \
            dictionary[index][WORD], \
            dictionary[index][CATEGORIES][0], \
            dictionary[index][INSTALLMENT]
        index += 1
    dump_json(dictionary, json_file)
    dictionary = load_json(json_file)
    pretty_print(dictionary, 0, 10)


def delete_entry(dictionary, some_id):
    entry_id = get_actual_id(dictionary, some_id)
    del dictionary[entry_id]
    restore_numeration(dictionary, int(entry_id))
    for index in range(len(dictionary)):
        if not get_actual_id(dictionary, index):
            print index, 'is missing!'


def restore_numeration(dictionary, deleted_index):
    current_index, next_index = deleted_index, deleted_index + 1
    while current_index < len(dictionary):
        dictionary[unicode(current_index)] = dictionary.pop(unicode(next_index))
        current_index += 1
        next_index += 1


def launch_entry_deleter(json_file, some_id):
    sure = raw_input("You sure you wish to delete entry " + some_id + '?')
    if sure != 'yes':
        print "Deletion cancelled"
        return
    dictionary = load_json(json_file)
    old_length = len(dictionary)
    delete_entry(dictionary, some_id)
    dump_json(dictionary, json_file)
    new_dictionary = load_json(json_file)
    new_length = len(new_dictionary)
    print "Dictionary is now %r entry(ies) shorter" % (old_length - new_length)




if __name__ == '__main__':
    launch_entry_deleter(JSON_FILE, 'κλαίω')
    pass
