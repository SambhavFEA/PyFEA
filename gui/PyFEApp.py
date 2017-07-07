import unicodedata
import fea
import numpy as np
import kivy
from kivy.lang import Builder

kivy.require('1.10.0')

from kivy.app import App
from kivy.app import Widget
from kivy.app import ObjectProperty

from kivy.core.window import Window

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.graphics import Rectangle, Color

from fea.FEModel import FEModel


class CustomInput(ButtonBehavior, TextInput):
    def on_release(self):
        self.focus = True
        super


class OpenDialog(Screen):
    but = ObjectProperty(None)
    txt_inp = ObjectProperty(None)
    fc = ObjectProperty(None)

    def open(self):
        location = self.fc.selection[0]
        part = FEModel(location)

        self.parent.current = 'model'
        self.parent.get_screen('model').part = part
        pass

class Blackboard(Widget):

    def __init__(self, **kwargs):
        super(Blackboard, self).__init__(**kwargs)

        self.update_grid()

        self.bind(size=self.update_grid)

    def update_grid(self,*args):
        elementsize=30
        y = int(round((self.height-elementsize) / elementsize))
        x = int(round(self.width / elementsize))
        with self.canvas:
            self.canvas.clear()
            Color(1, 1, 1)
            for i in range(0, x):
                for j in range(0, y):
                    Rectangle(pos=(i * elementsize, j * elementsize), size=(elementsize-1, elementsize-1))



class ModelScreen(Screen):
    part = None
    grid = ObjectProperty(None)

class PyFEApp(App):
    # Builder.load_file('PyFE.kv')

    def build(self):
        root = ScreenManager()
        root.add_widget(OpenDialog(name='open'))
        root.add_widget(ModelScreen(name='model'))
        root.current = 'model'

        openScreen = root.get_screen('open')

        modelScreen = root.get_screen('model')

        return root


if __name__ == '__main__':
    PyFEApp().run()
