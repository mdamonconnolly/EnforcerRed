'''
erLists is the function set to interact with the watch list file.
'''

import json, pathlib


def initialize(path=None):
    '''
    Initialize the list object
    '''
    obj = None

    if path != None:
        with open(path, 'r') as file:
            obj = json.load(file)
        return obj

    if pathlib.Path('lists.json').exists():
        with open('lists.json', 'r') as file:
            obj = json.load(file)
    else:
        obj = {}      
        with open('lists.json', 'w') as file:
            json.dump(obj, file)

    return obj
        
