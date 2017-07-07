import unicodedata
import fea
import kivy
from kivy.lang import Builder

kivy.require('1.10.0')

from kivy.app import App
from kivy.app import Widget
from kivy.app import ObjectProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput

from fea.FEModel import FEModel


class CustomInput(ButtonBehavior, TextInput):
    def on_release(self):
        self.focus = True
        super


class PyFEA(Widget):
    but = ObjectProperty(None)
    txt_inp = ObjectProperty(None)

    def open(self):
        location = self.txt_inp.text
        loc = unicode.encode(location, 'ascii')
        part = FEModel(loc)
        pass

    def set_focus(self):
        self.txt_inp.focus = True


class PyFEApp(App):
    Builder.load_file('PyFE.kv')

    def build(self):
        Window.size = (300, 100)
        return PyFEA()


if __name__ == '__main__':
    PyFEApp().run()
