import os
import json
import time
import threading

dir_path = os.path.dirname(os.path.realpath(__file__))

def cooldown(function, duration=int(30)):
    function.on_cooldown = False

    def sleeper():
        function.on_cooldown = True
        time.sleep(duration)
        function.on_cooldown = False

    async def wrapper(*args, **kwargs):
        if function.on_cooldown:
            print(f"Function {function.__name__} on cooldown")
        else:
            timer = threading.Thread(target=sleeper)
            await function(*args, **kwargs)
            timer.start()
    return wrapper


def get_channel():
    JSON_FILE = str(dir_path) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        CHAN = data['CHANNEL']
        return CHAN


def get_doxer():
    JSON_FILE = str(dir_path) + '/doxers.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        DOX = data['DOXERS']
        return DOX


def update_channel(value):
    JSON_FILE = str(dir_path) + f'/channels.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data['CHANNEL'] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def update_doxer(value):
    JSON_FILE = str(dir_path) + f'/doxers.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data['DOXERS'] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def get_namo(input, channel):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/namorados.json'
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
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/namorados.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        command.update(input)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4)


def delcmd(input, channel):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/namorados.json'
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
