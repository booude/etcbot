import os
import json


def loadutils(canal):
    with open(os.path.abspath('resources')+f'/{canal}/utils.json', encoding='utf8') as json_file:
        utils = json.load(json_file)
        return utils


def loadprizes(canal):
    with open(os.path.abspath('resources')+f'/{canal}/prizes.json', encoding='utf8') as json_file:
        prizes = json.load(json_file)
        return prizes
