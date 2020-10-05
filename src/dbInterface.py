import sqlite3

class dbInterface:

    """
    This is the interface to the database.
    TODO: Function for adding and changing records
    TODO: Function for merging 2 users
    TODO: Function to detect related accounts across multiple items, to merge them. 
    """

    def __init__(self, parent=None, dbFile='Data.db', logger=None):
        self.parent = parent
        self.logger = logger

        try:
            self.db = sqlite3.connect(dbFile)
            self.logger.out_message(f'Successfully connected to database: {dbFile}')
        except Exception as e:
            self.logger.out_error(f'Failed to connect to database: {e}')

        self.setupTables()

    
    def setupTables(self):
        """
        Makes sure the necessary tables are set up.
        """
        cursor = self.db.cursor()

        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                discord text,
                                reddit text,
                                notes text                                       
                                );        
                                """)

            cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
                                id integer PRIMARY KEY,
                                title text NOT NULL,
                                body text,
                                author text NOT NULL,
                                notes text,
                                FOREIGN KEY (user) REFERENCES users (id)
                                );
                                """)

            cursor.execute("""CREATE TABLE IF NOT EXISTS actions (
                                id integer PRIMARY KEY,
                                user text NOT NULL,
                                offense text NOT NULL,
                                responder text NOT NULL,
                                response text NOT NULL,
                                notes text,
                                FOREIGN KEY (user) REFERENCES users (id)
                                );
                                """)
            self.logger.out_message('Successfully set up tables.')
        except Exception as e:
            self.logger.out_error(f'Could not create tables: {e}')



    def add_user(self, *args):
        """
        The add_user function takes in a string to add, and adds it to the database.
        :param *args: List of usernames to be added. 
        """
        cursor = self.db.cursor()
        
        #for entry in args:
            #find if name already in db and connect up
