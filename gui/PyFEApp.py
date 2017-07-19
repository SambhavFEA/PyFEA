from kivy.config import Config

Config.set('graphics', 'resizable', False)

import numpy as np
import kivy
import math
from kivy.lang import Builder

from kivy.app import App
from kivy.app import Widget
from kivy.app import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.graphics import Rectangle, Color

from fea.FEModel import FEModel

kivy.require('1.10.0')


class CustomInput(ButtonBehavior, TextInput):
    def on_release(self):
        self.focus = True


class OpenDialog(Screen):
    but = ObjectProperty(None)
    txt_inp = ObjectProperty(None)
    fc = ObjectProperty(None)

    def open(self):
        location = self.fc.selection[0]
        part = FEModel(location)
        self.parent.get_screen('model').grid.part = part
        self.parent.get_screen('model').grid.load()
        self.parent.current = 'model'

        pass


class Blackboard(ButtonBehavior, Widget):
    part = None
    rec = None
    elementsize = 30
    xPos = None
    yPos = None
    refresh = None
    pressed = None

    def update_grid(self, *args):
        element_size = self.elementsize
        with self.canvas:
            self.canvas.clear()
            for i in range(0, self.xPos):
                for j in range(0, self.yPos):
                    Color(self.rec[i, j, 0], self.rec[i, j, 1], self.rec[i, j, 2])
                    Rectangle(pos=(i * element_size, j * element_size), size=(element_size - 1, element_size - 1))

    def select_rec(self, *args):
        pos = Window.mouse_pos
        x = int(math.floor(pos[0] / self.elementsize))
        y = int(math.floor(pos[1] / self.elementsize))
        if self.parent.parent.ids.tbutPart.state == 'down':
            self.rec[x, y, :] = [0, 0, 1]
        self.pressed = Clock.schedule_once(self.select_rec, 0.001)

    def stop_press(self):
        Clock.unschedule(self.pressed)

    def load(self):
        ele_size=np.shape(self.part.ele)
        for i in range(ele_size[0]):
            pos = self.part.nodes[int(self.part.ele[i,0]) - 1,:]
            self.rec[int(pos[0]), int(pos[1]),:] = [0, 0, 1]


class ModelScreen(Screen):
    grid = ObjectProperty(None)

    def open_screen(self):
        self.parent.current = 'open'


class PyFEApp(App):
    # Builder.load_file('PyFE.kv')

    def build(self):
        Window.size = (600, 640)
        root = ScreenManager()
        root.add_widget(OpenDialog(name='open'))
        root.add_widget(ModelScreen(name='model'))
        root.current = 'model'

        openScreen = root.get_screen('open')

        modelScreen = root.get_screen('model')

        black_board = modelScreen.grid
        element_size = black_board.elementsize
        black_board.yPos = int(round(black_board.height / element_size))
        black_board.xPos = int(round(black_board.width / element_size))
        black_board.rec = np.ones((black_board.xPos, black_board.yPos,3))
        black_board.refresh = Clock.schedule_interval(black_board.update_grid, 0.1)
        return root


if __name__ == '__main__':
    PyFEApp().run()
