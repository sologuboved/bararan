# -*- coding: utf-8 -*-

import csv
import json
import random

TRANSLATION = 'translation'
ARTICLE = 'articles'
WORD = 'word'
CATEGORIES = 'categories'
INSTALLMENT = 'installment'
EXAMPLE = 'example'
GRAMMAR = 'grammar'
MISC = 'misc'
FIELDS = [WORD, ARTICLE, TRANSLATION, CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, MISC]

CSV_FILE = 'greek_words.csv'
JSON_FILE = 'json_lexilogio.json'
JSON_FILE_COPY = 'json_lexilogio_copy.json'

YES = 'yes'


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


def dump_json(dictionary, json_file):
    with open(json_file, 'w') as fp:
        json.dump(dictionary, fp)


def load_json(json_file):
    with open(json_file) as data:
        dictionary = json.load(data)
        return dictionary


def pretty_print(dictionary, start=0, end='all'):
    length = len(dictionary)
    assert start < length, "Start %d not in range [0, %d)" % (start, length)
    if end:
        if end == 'all':
            for index in range(start, len(dictionary)):
                print_entry(dictionary, index)
        else:
            assert start < end < length, "End %d not in range (%d, %d)" % (end, start, length)
            while start < end:
                print_entry(dictionary, start)
                start += 1
    else:
        print_entry(dictionary, start)


def launch_category_printer(json_file, category):
    dictionary = load_json(json_file)
    print_by_category(dictionary, category)


def print_by_category(dictionary, category):
    count = 0
    try:
        category = unicode(category, 'utf-8')
        for entry_id in dictionary:
            if category in dictionary[entry_id][CATEGORIES]:
                print_entry(dictionary, entry_id)
                count += 1
        print count, "item(s) in '" + category + "'"
    except TypeError as e:
        print e


def look_up(json_file, word):
    dictionary = load_json(json_file)
    print_by_word(dictionary, word)


def print_by_word(dictionary, word):
    try:
        word = unicode(word, 'utf-8')
        for entry_id in dictionary:
            if word == dictionary[entry_id][WORD]:
                print_entry(dictionary, entry_id)
                break
    except TypeError as e:
        print e


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


def create_test_dictionary(json_file, num_entries, start=None):
    test_dictionary = dict()
    basic_dictionary = load_json(json_file)
    possible_range = len(basic_dictionary) - num_entries
    if start is None:
        start = random.randrange(0, possible_range + 1)
    else:
        assert start < possible_range, "(%d, %d) does not fit in range" % (start, start + num_entries)
    test_id = 0
    for index in range(start, start + num_entries):
        test_entry = dict()
        basic_entry_id = get_actual_id(basic_dictionary, index)
        basic_entry = basic_dictionary[basic_entry_id]
        for field in FIELDS:
            item = basic_entry[field]
            if type(item) == list:
                test_entry[field] = item[:]
            else:
                test_entry[field] = item
        test_dictionary[unicode(test_id)] = test_entry
        test_id += 1
    return test_dictionary


def rename_field(dictionary, old_field, new_field):
    for entry_id in dictionary:
        entry = dictionary[entry_id]
        entry[new_field] = entry[old_field]
        del entry[old_field]


def launch_field_renamer(json_file, old_field, new_field):
    dictionary = load_json(json_file)
    rename_field(dictionary, old_field, new_field)
    dump_json(dictionary, json_file)


def launch_empty_article_deleter(json_file):
    dicionary = load_json(json_file)
    delete_empty_articles(dicionary)
    dump_json(dicionary, json_file)


def delete_empty_articles(dictionary):
    for entry_id in dictionary:
        entry = dictionary[entry_id]
        if entry[ARTICLE][0] == u'':
            entry[ARTICLE] = list()


def launch_article_shifter(json_file):
    dictionary = load_json(json_file)
    shift_articles(dictionary)
    dump_json(dictionary, json_file)


def shift_articles(dictionary):
    for entry_id in dictionary:
        entry = dictionary[entry_id]
        categories = entry[CATEGORIES]
        not_diafora = not unicode('διάφορα', 'utf-8') in categories
        not_verb = not unicode('ρήματα', 'utf-8') in categories
        not_adverb = not unicode('επιρρήματα', 'utf-8') in categories
        not_adjective = not unicode('επίθετα', 'utf-8') in categories
        no_article = not entry[ARTICLE]
        if no_article and not_diafora and not_verb and not_adverb and not_adjective:
            word = entry[WORD]
            elements = word.strip().split()
            potential_article = elements[0]
            articles = {unicode('ο', 'utf-8'),
                        unicode('η', 'utf-8'),
                        unicode('το', 'utf-8'),
                        unicode('ο/η', 'utf-8'),
                        unicode('οι', 'utf-8'),
                        unicode('τα', 'utf-8')}
            if potential_article in articles:
                entry[ARTICLE].append(potential_article)
                entry[WORD] = ' '.join(elements[1:])


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


def find_duplicates(json_file):
    dictionary = load_json(json_file)
    freqs = dict()
    for entry_id in dictionary:
        word = dictionary[entry_id][WORD]
        if word in freqs:
            duplicate = freqs[word]
            duplicate[0] += 1
            duplicate[1].append(entry_id)
        else:
            freqs[word] = [1, [entry_id]]
    duplicates = {word: val[1] for word, val in freqs.items() if val[0] > 1}
    for duplicate in duplicates:
        print duplicate, duplicates[duplicate]


def launch_entry_deleter_or_merger(json_file, *args):
    dictionary = load_json(json_file)
    old_length = len(dictionary)
    if len(args) == 1:
        entry_id = get_actual_id(dictionary, args[0])
        sure = raw_input("Are you sure you wish to delete entry " + dictionary[entry_id][WORD] + "? ")
        if sure != YES:
            print "Deletion cancelled"
            return
        if delete_entry(dictionary, entry_id):
            dump_json(dictionary, json_file)
    elif len(args) == 2:
        some_id1, some_id2 = args
        entry_id1, entry_id2 = get_actual_id(dictionary, some_id1), get_actual_id(dictionary, some_id2)
        if entry_id1 and entry_id2:
            if entry_id1 == entry_id2:
                print "It is the same entry with id", entry_id1
                return
            prompt = "Are you sure you wish to merge entries " + dictionary[entry_id1][WORD] + " and " + \
                     dictionary[entry_id2][WORD] + "? "
            sure = raw_input(prompt)
            if sure != YES:
                print "Merge cancelled"
                return
            if merge_entries(dictionary, entry_id1, entry_id2):
                dump_json(dictionary, json_file)
        else:
            if entry_id1:
                wrong_entry = entry_id2
            elif entry_id2:
                wrong_entry = entry_id1
            else:
                print "Entries with id", entry_id1, entry_id2, "do not exist"
                return
            print "Entry with id", wrong_entry, "does not exist"
            return
    else:
        print "Wrong number of ids:", len(args)
        return
    new_dictionary = load_json(json_file)
    new_length = len(new_dictionary)
    print "Dictionary is now %r entry(ies) shorter" % (old_length - new_length)


def merge_entries(dictionary, entry_id1, entry_id2):
    entry1 = dictionary[entry_id1]
    entry2 = dictionary[entry_id2]
    entry2_fields = [entry2[field] for field in FIELDS]
    for index in range(len(FIELDS)):
        field = FIELDS[index]
        entry1_field = entry1[field]
        if type(entry1_field) == list:
            entry2_field = entry2_fields[index]
            for item in entry2_field:
                if item not in entry1_field:
                    entry1_field.append(item)
    return delete_entry(dictionary, entry_id2)


def delete_entry(dictionary, entry_id):
    if entry_id:
        del dictionary[entry_id]
        restore_numeration(dictionary, int(entry_id))
        for index in range(len(dictionary)):
            if not get_actual_id(dictionary, index):
                print index, 'is missing!'
                return False
        return True
    else:
        print "Entry with id", entry_id, "does not exist"
        return False


def restore_numeration(dictionary, deleted_index):
    current_index, next_index = deleted_index, deleted_index + 1
    while current_index < len(dictionary):
        dictionary[unicode(current_index)] = dictionary.pop(unicode(next_index))
        current_index += 1
        next_index += 1


def launch_correction_maker(json_file, some_id, field, correction):
    dictionary = load_json(json_file)
    entry_id = get_actual_id(dictionary, some_id)
    if not entry_id:
        print "No such entry"
        return
    print_entry(dictionary, entry_id)
    sure = raw_input("Are you sure you wish to modify field '" + field + "' of this entry? ")
    if sure != 'yes':
        print "Correction cancelled"
        return
    if make_correction(dictionary, entry_id, field, correction):
        dump_json(dictionary, json_file)
    print 'Now:',
    print_entry(dictionary, entry_id)


def make_correction(dictionary, entry_id, field, correction):
    if not is_correct_type(field, correction):
        print 'unprocessed', correction, "does not go into", field
        return False
    if field == WORD or field == INSTALLMENT:
        correction = unicode(str(correction), 'utf-8')
    else:
        correction = map(lambda x: unicode(str(x), 'utf-8'), correction)
    if not is_unicode(field, correction):
        print 'processed', correction, "does not go into", field
        return False
    dictionary[entry_id][field] = correction
    return True


def is_correct_type(field, correction):
    if field not in FIELDS:
        print "Non-existent field"
        return False
    if field == WORD:
        if type(correction) != str:
            print "Should have been a string"
            return False
        else:
            return True
    if field == INSTALLMENT:
        if type(correction) != int:
            print "Should have been an integer"
            return False
        else:
            return True
    if type(correction) != list:
        print "Should have been a list"
        return False
    return True


def is_unicode(field, correction):
    if field == WORD or field == INSTALLMENT:
        if type(correction) != unicode:
            print "Should have been a unicode string"
            return False
        else:
            return True
    for item in correction:
        if type(item) != unicode:
            print item, "is not unicode but", type(item)
            return False
    return True


def launch_category_adder(json_file, index):
    dictionary = load_json(json_file)
    stopped_at = add_categories(dictionary, index)
    dump_json(dictionary, json_file)
    print "Stopped at", stopped_at


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


if __name__ == '__main__':
    # launch_correction_maker(JSON_FILE, 'γιατί', CATEGORIES, ['βοηθητικά'])
    # launch_category_printer(JSON_FILE, 'διάφορα')
    look_up(JSON_FILE, 'γιατί')