# -*- coding: utf-8 -*-

import requests
import json
import csv

TRANSLATION = 'translation'
ARTICLE = 'articles'
WORD = 'word'
CATEGORIES = 'categories'
INSTALLMENT = 'installment'
EXAMPLE = 'example'
GRAMMAR = 'grammar'
MISC = 'misc'
JSON_FILE = 'json_lexilogio.json'
JSON_URL = 'https://raw.githubusercontent.com/sologuboved/bararan/master/json_lexilogio.json'


def load_json_from_url(json_url):
    raw = requests.get(json_url)
    dictionary = raw.json()
    return dictionary


def load_json_from_file(json_file):
    with open(json_file) as data:
        dictionary = json.load(data)
        return dictionary


def extract_values(dictionary):
    extracted = list()
    for entry in dictionary:
        print type(entry)
        temp_dict = {TRANSLATION: ', '.join(dictionary[entry][TRANSLATION]).encode('utf-8'),
                     ARTICLE: ', '.join(dictionary[entry][ARTICLE]).encode('utf-8'),
                     WORD: dictionary[entry][WORD].encode('utf-8'),
                     CATEGORIES: ', '.join(dictionary[entry][CATEGORIES]).encode('utf-8'),
                     INSTALLMENT: dictionary[entry][INSTALLMENT].encode('utf-8'),
                     EXAMPLE: ', '.join(dictionary[entry][EXAMPLE]).encode('utf-8'),
                     GRAMMAR: ', '.join(dictionary[entry][GRAMMAR]).encode('utf-8'),
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
    csv_keys = [TRANSLATION, ARTICLE, WORD, CATEGORIES, INSTALLMENT, EXAMPLE, GRAMMAR, MISC]
    # my_dict = load_json_from_file(JSON_FILE)
    my_dict = load_json_from_url(JSON_URL)
    values = extract_values(my_dict)
    write_csv(values, csv_keys, 'extracted_lexilogio')
