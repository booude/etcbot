import os
import json


def loadutils(canal):
    with open(os.path.abspath('resources')+f'/{canal}/utils.json', encoding='utf8') as json_file:
        utils = json.load(json_file)
        return utils


def count(user, canal):
    with open(os.path.abspath('resources')+f'/{canal}/utils.json', encoding='utf8') as json_file:
        counter = json.load(json_file)
    try:
        counter[f'{user}'] += 1
    except KeyError:
        counter.update({user: 1})
    with open(os.path.abspath('resources')+f'/{canal}/utils.json', 'w', encoding='utf-8') as json_file:
        json.dump(counter, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)
