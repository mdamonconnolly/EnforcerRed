from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder

#Builder.load_file('./MainWindow.kv')

class MainWindow(TabbedPanel):
    pass

class erKui(App):

    def __init__(self):
        App.__init__(self)
        print("Instantiated...")

    def build(self):
        return MainWindow()

if __name__ == '__main__':

    erKui().run()
