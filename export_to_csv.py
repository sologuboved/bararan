# -*- coding: utf-8 -*-

import requests
import json
import csv

# По умолчанию - греческий. Для переключения на армянский присвоить ARM значение True

ARM = False

TRANSLATION = 'translation'
ARTICLE = 'articles'
WORD = 'word'
CATEGORIES = 'categories'
INSTALLMENT = 'installment'
EXAMPLE = 'example'
GRAMMAR = 'grammar'
IDIOMS = 'idioms'
MISC = 'misc'
JSON_FILE = 'json_lexilogio.json'
JSON_URL = 'https://raw.githubusercontent.com/sologuboved/bararan/master/json_lexilogio.json'
LANGUAGE = 'greek'
OUTPUT_FILE_NAME = 'exported_lexilogio'
CSV_KEYS = [TRANSLATION, ARTICLE, WORD, CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, MISC]
if ARM:
    JSON_FILE = 'json_bararan.json'
    LANGUAGE = 'armenian'
    OUTPUT_FILE_NAME = 'exported_bararan'
    CSV_KEYS = [TRANSLATION, WORD, CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, IDIOMS, MISC]



def load_json_from_url(json_url):
    raw = requests.get(json_url)
    dictionary = raw.json()
    return dictionary


def load_json_from_file(json_file):
    with open(json_file) as data:
        dictionary = json.load(data)
        return dictionary


def extract_values(dictionary, lang):
    extracted = list()

    if lang == 'greek':

        # Для греческого

        for entry in dictionary:
            temp_dict = {TRANSLATION: ', '.join(dictionary[entry][TRANSLATION]).encode('utf-8'),
                         ARTICLE: ', '.join(dictionary[entry][ARTICLE]).encode('utf-8'),
                         WORD: dictionary[entry][WORD].encode('utf-8'),
                         CATEGORIES: ', '.join(dictionary[entry][CATEGORIES]).encode('utf-8'),
                         INSTALLMENT: dictionary[entry][INSTALLMENT].encode('utf-8'),
                         EXAMPLE: ', '.join(dictionary[entry][EXAMPLE]).encode('utf-8'),
                         GRAMMAR: ', '.join(dictionary[entry][GRAMMAR]).encode('utf-8'),
                         MISC: ', '.join(dictionary[entry][MISC]).encode('utf-8')}
            extracted.append(temp_dict)

    elif lang == 'armenian':

    # Для армянского

        for entry in dictionary:
            temp_dict = {TRANSLATION: ', '.join(dictionary[entry][TRANSLATION]).encode('utf-8'),
                         WORD: dictionary[entry][WORD].encode('utf-8'),
                         CATEGORIES: ', '.join(dictionary[entry][CATEGORIES]).encode('utf-8'),
                         INSTALLMENT: dictionary[entry][INSTALLMENT].encode('utf-8'),
                         EXAMPLE: ', '.join(dictionary[entry][EXAMPLE]).encode('utf-8'),
                         GRAMMAR: ', '.join(dictionary[entry][GRAMMAR]).encode('utf-8'),
                         IDIOMS: ', '.join(dictionary[entry][IDIOMS]).encode('utf-8'),
                         MISC: ', '.join(dictionary[entry][MISC]).encode('utf-8')}
            extracted.append(temp_dict)
    return extracted


def write_csv(lst_of_dicts, header_list, file_name):

    # Записать извлеченные данные в файл CSV

    with open('{}.csv'.format(file_name), 'wb') as handler:
        print 'Writing...'
        writer = csv.DictWriter(handler, fieldnames=header_list)
        writer.writeheader()
        for item in lst_of_dicts:
            writer.writerow(item)
        print 'Done!'


if __name__ == '__main__':

    # my_dict = load_json_from_url(JSON_URL)
    my_dict = load_json_from_file(JSON_FILE)
    values = extract_values(my_dict, LANGUAGE)
    write_csv(values, CSV_KEYS, OUTPUT_FILE_NAME)