import io
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_channel():
    JSON_FILE = str(dir_path) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        CHAN = data['CHANNEL']
        return CHAN


def get(input, channel):
    COMMAND_FILE = str(dir_path) + f'/namorados.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        if input == '@all':
            return command
        else:
            key_list = list(command.keys())
            val_list = list(command.values())
            pos = val_list.index(input)
            input = key_list[pos]
            return command[f'{input}']


def add(input, channel):
    COMMAND_FILE = str(dir_path) + f'/namorados.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        command.update(input)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4)


def delcmd(input, channel):
    COMMAND_FILE = str(dir_path) + f'/namorados.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        key_list = list(command.keys())
        val_list = list(command.values())
        pos = val_list.index(input)
        input = key_list[pos]
        result = command.pop(input, None)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4)
        return result
