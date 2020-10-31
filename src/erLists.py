"""
erLists is the function set to interact with the watch list file.
TODO: Create watch list functionality for v0.4.0
"""

import json, pathlib


def initialize(path=None):
    """
    Initialize the list object
    """
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


def addList():
    """
    Add a list. Needs custom function to create its internal meta object
    """
    pass


def listTables():
    """
    List the currently loaded tables and their internal "meta" object data
    """
    pass
        
