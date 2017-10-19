from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput


class NumericInput(ButtonBehavior, TextInput):
    def on_release(self):
        self.focus = True