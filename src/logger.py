import arrow

"""
The Logger module contains all of the output functionality. Consider name change.
"""

class Logger:

    def __init__(self, debug=False, log=False, parent=None):
        print("Interface Initialized")
        self.parent = parent
        self.debugMode = debug
        self.textLog = log

        self.printRunStamp()


    def printRunStamp(self):
        time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print(f'\n\nEnforcer Red started!\nTime: {time}\nVersion: {self.parent.version}\n')

        if self.textLog == False:
            return

        with open('Log.txt', 'a') as file:
            file.write(
               f'\n\n\n================\nEnforcer: Red started!\nTime: {time}\nVersion: {self.parent.version}\n================' 
            )


    def out_message(self, text):
        """
        Print a message to the console and, if applicable, output as log.
        This is for general purpose log messages.
        """

        time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print(f"{self.CLEAR}{time}: {text}")

        if self.textLog == False:
            return

        try:
            with open('Log.txt', 'a') as file:
                file.write(
                    f'\n{time}: {text}'
                )
        except Exception as e:
            print(f"Exception: {e}")

            
    def out_success(self, text):
        """
        Print message to the console and log in green.
        """
        time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print(f"{self.GREEN}{time}: {text}{self.CLEAR}")

        if self.textLog == False:
            return

        try: 
            with open('Log.txt', 'a') as file:
                    file.write(
                        f'\n{time}: {text}'
                    )
        except Exception as e:
            print(f"Exception: {e}")

    def out_warning(self, text):
        """
        Print a warning to the console. This will show up in yellow.
        This is for anything that needs non-immediate attention.
        """
        time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print(f"{self.YELLOW}{time}: {text}{self.CLEAR}")

        if self.textLog == False:
            return

        try:
            with open('Log.txt', 'a') as file:
                file.write(
                    f'\n{time} : *WARN* - {text}'
                )
        except Exception as e:
            print(f'Exception: {e}')

        
    def out_error(self, text):
        """
        Print an alert in red to the console.
        This is for immediate-attention issues.
        """
        time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print(f"{self.RED}{time}: {text}{self.CLEAR}")

        if self.textLog == False:
            return

        try:
            with open('Log.txt', 'a') as file:
                file.write(f'\n\t\t\t\t\t/////////////')
                file.write(
                    f'\n{time}: ===ALERT=== {text}'
                )
                file.write(f'\n\t\t\t\t\t/////////////')
        except Exception as e:
            print(f'Exception: {e}')


    def out_meta(self, text):
        """
        Output debug information regarding the bot in blue. 
        """
        if self.debugMode == False:
            return

        time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print(f'{self.BLUE}{time}: {text}{self.CLEAR}')

        if self.textLog == False:
            return

        try:
            with open('Log.txt', 'a') as file:
                file.write(
                    f'\n{time} - DEBUG: {text}'
                )
        except Exception as e:
            print(f'Exception: {e}')

    CLEAR = '\033[0m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
