import kivy
import numpy as np
from kivy import metrics
from kivy.app import App
from kivy.app import ObjectProperty
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from fea.FEModel.FELinearModel import FEModel

from NumericInput import NumericInput
from DropDownButton import SolnProcDropDown
from Blackboard import Blackboard

Config.set('graphics', 'resizable', False)

kivy.require('1.10.0')


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


class ModelScreen(Screen):
    grid = ObjectProperty(None)
    material_type = ObjectProperty(None)
    row_one = ObjectProperty(None)
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
        pixel_x = metrics.dp(600)
        pixel_y = metrics.dp(680)
        Window.size = (pixel_x, pixel_y)
        root = ScreenManager()
        root.add_widget(OpenDialog(name='open'))
        root.add_widget(ModelScreen(name='model'))
        root.add_widget(MaterialScreen(name='material'))
        root.add_widget(ResultScreen(name='result'))
        root.current = 'model'

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
