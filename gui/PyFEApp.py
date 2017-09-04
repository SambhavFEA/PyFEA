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
    rectangles = None

    force_v = {}
    force_h = {}
    perma_force_v = {}
    perma_force_h = {}

    support_v = {}
    support_h = {}
    perma_support_v = {}
    perma_support_h = {}

    force_size = 5
    support_size = 5

    element_size = 30
    xPos = None
    yPos = None
    refresh = None
    pressed = None
    go_right = True
    go_up = True
    mouse_pos_last_press = None

    def update_grid(self, *args):
        element_size = self.element_size
        with self.canvas:
            self.canvas.clear()

            # drawing the rectangles
            for i in range(0, self.xPos):
                for j in range(0, self.yPos):
                    Color(self.rectangles[i, j, 0], self.rectangles[i, j, 1], self.rectangles[i, j, 2])
                    Rectangle(pos=(i * element_size, j * element_size), size=(element_size - 1, element_size - 1))

            force_size = self.force_size
            Color(1, 0, 0)
            self.update_constraints(force_size, self.force_v, self.force_h, self.perma_force_v, self.perma_force_h)

            support_size = self.support_size
            Color(0, 1, 0)
            self.update_constraints(support_size, self.support_v, self.support_h, self.perma_support_v,
                                    self.perma_support_h)

    def update_constraints(self, constraint_size, temp_v, temp_h, perma_v, perma_h):

        # drawing permanent vertical constraints
        length = len(perma_v)
        listofkeys = perma_v.keys()
        if length != 0:
            for i in range(length):
                x = listofkeys[i][0]
                y = listofkeys[i][1]
                Rectangle(pos=(
                    (x * self.element_size) - (constraint_size / 2), (y * self.element_size) - (constraint_size / 2)),
                    size=(constraint_size, self.element_size - 1))

        # drawing permanent horizontal constraints
        length = len(perma_h)
        listofkeys = perma_h.keys()
        if length != 0:
            for i in range(length):
                x = listofkeys[i][0]
                y = listofkeys[i][1]
                Rectangle(pos=(
                    (x * self.element_size) - (constraint_size / 2), (y * self.element_size) - (constraint_size / 2)),
                    size=(self.element_size - 1, constraint_size))

        # drawing vertical constraints
        length = len(temp_v)
        listofkeys = temp_v.keys()
        if length != 0:
            for j in range(length):
                if temp_v[listofkeys[0]][2] == 0 or temp_v[listofkeys[j]][2] <= length:
                    temp_v[listofkeys[j]][2] = length + 1
            for i in range(length):
                y = listofkeys[i]
                x = temp_v[y][1]
                Rectangle(pos=(
                    (x * self.element_size) - (constraint_size / 2), (y * self.element_size) - (constraint_size / 2)),
                    size=(constraint_size, self.element_size - 1))
                if self.go_right:
                    if self.rectangles[x, y, 1] != 0:
                        if self.pressed.is_triggered == 0:
                            val = temp_v[y]
                            if (x + 1) < self.xPos:
                                temp_v[y][1] = val[1] + 1
                            else:
                                del temp_v[y]
                    else:
                        perma_v[(x, y)] = temp_v[y][0] / temp_v[y][2]
                        del temp_v[y]
                else:
                    if self.rectangles[x - 1, y, 1] != 0:
                        if self.pressed.is_triggered == 0:
                            val = temp_v[y]
                            if (x - 1) >= 0:
                                temp_v[y][1] = val[1] - 1
                            else:
                                del temp_v[y]
                    else:
                        perma_v[(x, y)] = temp_v[y][0] / temp_v[y][2]
                        del temp_v[y]

        # drawing horizontal constraints
        length = len(temp_h)
        listofkeys = temp_h.keys()

        if length != 0:
            for j in range(length):
                if temp_h[listofkeys[j]][2] == 0 or temp_h[listofkeys[j]][2] <= length:
                    temp_h[listofkeys[j]][2] = length + 1
            for i in range(length):
                x = listofkeys[i]
                y = temp_h[x][1]
                Rectangle(pos=(
                    (x * self.element_size) - (constraint_size / 2), (y * self.element_size) - (constraint_size / 2)),
                    size=(self.element_size - 1, constraint_size))
                if self.go_up:
                    if self.rectangles[x, y, 1] != 0:
                        if self.pressed.is_triggered == 0:
                            val = temp_h[x]
                            if (y + 1) < self.xPos:
                                temp_h[x][1] = val[1] + 1
                            else:
                                del temp_h[x]
                    else:
                        perma_h[(x, y)] = temp_h[x][0] / temp_h[x][2]
                        del temp_h[x]
                else:
                    if self.rectangles[x, y - 1, 1] != 0:
                        if self.pressed.is_triggered == 0:
                            val = temp_h[x]
                            if (y - 1) >= 0:
                                temp_h[x][1] = val[1] - 1
                            else:
                                del temp_h[x]
                    else:
                        perma_h[(x, y)] = temp_h[x][0] / temp_h[x][2]
                        del temp_h[x]
        pass

    def select_rec(self, *args):
        pos = Window.mouse_pos
        if self.mouse_pos_last_press is None:
            self.mouse_pos_last_press = pos
        x = int(math.floor(pos[0] / self.element_size))
        y = int(math.floor(pos[1] / self.element_size))
        if self.parent.parent.ids.tbutPart.state == 'down':
            # taking inputs for rectangles/part body
            self.rectangles[x, y, :] = [0, 0, 1]
        elif self.parent.parent.ids.tbutForceV.state == 'down':
            # taking inputs for vertical forces
            if self.rectangles[x, y, 1] != 0:
                self.force_v[y] = [45, x, 0]  # Enter value of Force
        elif self.parent.parent.ids.tbutForceH.state == 'down':
            # taking inputs for horizontal forces
            if self.rectangles[x, y, 1] != 0:
                self.force_h[x] = [45, y, 0]  # Enter value of Force
        elif self.parent.parent.ids.tbutSupportV.state == 'down':
            # taking inputs for vertical supports
            if self.rectangles[x, y, 1] != 0:
                self.support_v[y] = [0, x, 0]
        elif self.parent.parent.ids.tbutSupportH.state == 'down':
            # taking inputs for horizontal supports
            if self.rectangles[x, y, 1] != 0:
                self.support_h[x] = [0, y, 0]

        self.pressed = Clock.schedule_once(self.select_rec, 0.001)

    def stop_press(self):
        pos = Window.mouse_pos
        if pos[0] - self.mouse_pos_last_press[0] >= 0:
            self.go_right = True
        else:
            self.go_right = False

        if pos[1] - self.mouse_pos_last_press[1] >= 0:
            self.go_up = True
        else:
            self.go_up = False

        self.mouse_pos_last_press = None
        Clock.unschedule(self.pressed)

    def load(self):
        ele_size = np.shape(self.part.ele)
        for i in range(ele_size[0]):
            pos = self.part.nodes[int(self.part.ele[i, 0]) - 1, :]
            self.rectangles[int(pos[0]), int(pos[1]), :] = [0, 0, 1]


class ModelScreen(Screen):
    grid = ObjectProperty(None)
    fe_model = None

    def open_screen(self):
        self.parent.current = 'open'

    def material_screen(self):
        self.parent.current = 'material'

    def save(self):
        # This is only for quad node element
        model_screen = self.parent.get_screen('model')
        material_screen = self.parent.get_screen('material')

        material = np.zeros([2, 1])  # No. of material properties are hardcoded here.
        material[0] = float(material_screen.material1.text)
        material[1] = float(material_screen.material2.text)

        ele_size = model_screen.grid.element_size
        recs = model_screen.grid.rectangles
        num_of_rectangles = np.shape(recs)
        elements_list = []  # elements list, [element no, node1, node 2, node3, node 4]
        nodes_dics = {}  # nodes dictionary, key=(x,y) , value = node number
        n = 0  # node number
        e = 0  # element number
        for i in range(model_screen.grid.xPos):
            for j in range(model_screen.grid.yPos):
                color = recs[i, j, :]
                if (color == [0, 0, 1]).all():
                    if not (nodes_dics.has_key((i, j))):
                        nodes_dics[(i, j)] = n
                        n = n + 1
                    if not (nodes_dics.has_key((i + 1, j))):
                        nodes_dics[(i + 1, j)] = n
                        n = n + 1
                    if not (nodes_dics.has_key((i, j + 1))):
                        nodes_dics[(i, j + 1)] = n
                        n = n + 1
                    if not (nodes_dics.has_key((i + 1, j + 1))):
                        nodes_dics[(i + 1, j + 1)] = n
                        n = n + 1
                    elements_list.append(np.array(
                        [e, nodes_dics[(i, j)], nodes_dics[(i + 1, j)], nodes_dics[(i, j + 1)],
                         nodes_dics[(i + 1, j + 1)]]))
                    e = e + 1
        elements = np.asarray(elements_list)
        nodes = np.zeros([len(nodes_dics), 3])
        nodes[:, 1:3] = ele_size * np.array(nodes_dics.keys())
        nodes[:, 0] = np.array(nodes_dics.values())
        temp_pos = nodes[:, 0].argsort()
        nodes = nodes[temp_pos, :]

        force_h = model_screen.grid.perma_force_h
        force_v = model_screen.grid.perma_force_v
        support_h = model_screen.grid.perma_support_h
        support_v = model_screen.grid.perma_support_v

        force_dics = {}
        support_dics = {}

        length = len(force_h)
        list_of_keys = force_h.keys()
        for i in range(length):
            force_dics[list_of_keys[i]] = [nodes_dics[list_of_keys[i]], 0, force_h[list_of_keys[i]]]

        length = len(force_v)
        list_of_keys = force_v.keys()
        for i in range(length):
            if force_dics.has_key(list_of_keys[i]):
                force_dics[list_of_keys[i]][1] = force_v[list_of_keys[i]]
            else:
                force_dics[list_of_keys[i]] = [nodes_dics[list_of_keys[i]], force_v[list_of_keys[i]], 0]

        length = len(support_h)
        list_of_keys = support_h.keys()
        for i in range(length):
            support_dics[i] = [nodes_dics[list_of_keys[i]], 1, support_h[list_of_keys[i]]]

        length1 = len(support_v)
        list_of_keys = support_v.keys()
        for i in range(length1):
            support_dics[length + i] = [nodes_dics[list_of_keys[i]], 0, support_v[list_of_keys[i]]]

        force = np.array(force_dics.values())
        support = np.array(support_dics.values())

        self.fe_model = FEModel(elements[:, 1:5], nodes[:, 1:3], material, force, support)

        self.parent.current = 'result'

class MaterialScreen(Screen):
    material1 = ObjectProperty(None)
    material2 = ObjectProperty(None)

    def open_screen(self):
        self.parent.current = 'material'

    def model_screen(self):
        self.parent.current = 'model'


class ResultScreen(Screen):
    def open_screen(self):
        self.parent.current = 'result'

    def solve(self):
        model_screen = self.parent.get_screen('model')
        fe_model = model_screen.fe_model
        pass


class PyFEApp(App):
    # Builder.load_file('PyFE.kv')

    def build(self):
        Window.size = (600, 640)
        root = ScreenManager()
        root.add_widget(OpenDialog(name='open'))
        root.add_widget(ModelScreen(name='model'))
        root.add_widget(MaterialScreen(name='material'))
        root.add_widget(ResultScreen(name='result'))
        root.current = 'result'

        open_screen = root.get_screen('open')

        model_screen = root.get_screen('model')

        material_screen = root.get_screen('material')

        result_screen = root.get_screen('result')

        black_board = model_screen.grid
        element_size = black_board.element_size
        black_board.yPos = int(round(black_board.height / element_size))
        black_board.xPos = int(round(black_board.width / element_size))
        black_board.rectangles = np.ones((black_board.xPos, black_board.yPos, 3))
        black_board.refresh = Clock.schedule_interval(black_board.update_grid, 0.1)
        return root


if __name__ == '__main__':
    PyFEApp().run()
