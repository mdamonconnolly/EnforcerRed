import sqlite3

class dbInterface:
    """
    The dbInterface class will act as an interface to abstract the sqlite3 stuff.
    """
    def __init__(self, parent=None):
        self.parent = parent

        #self.cdb = sqlite3.connect('data.db')


    #def add_to_db(self, table, data):
        """
        This adds data to a target table.
        """
