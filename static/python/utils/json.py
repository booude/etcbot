import os
import json


def loadutils(canal):
    with open(os.path.abspath('resources')+f'/{canal}/utils.json', encoding='utf8') as json_file:
        utils = json.load(json_file)
        return utils
