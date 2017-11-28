from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import fea.FEStiffness
import fea.FESolnProc
import inspect


class DropDownButton(Button):
    def __init__(self, **kwargs):
        super(DropDownButton, self).__init__(**kwargs)
        self.drop_list = DropDown()

        if kwargs.has_key('type'):
            types = kwargs['type']
        else:
            types = ['empty']

        if kwargs.has_key('module') and kwargs.has_key('widget'):
            mod = __import__(kwargs['module'], fromlist=kwargs['widget'])
            widget_name = kwargs['widget']
        else:
            mod = __import__('kivy.uix.button', fromlist=['Button'])
            widget_name = 'Button'

        for i in types:
            attr = getattr(mod, widget_name)
            btn = attr(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))


class MaterialDropDown(DropDownButton):
    def __init__(self, **kwargs):
        '''
        clss = inspect.getmembers(fea.FEStiffness, inspect.isclass)
        cll_name = []
        for index in range(len(clss) - 1):
            cll_name.append(clss[index + 1][0])
        kwargs['type'] = cll_name
        kwargs['module'] = 'kivy.uix.button'
        kwargs['widget'] = 'Button'
        '''
        super(MaterialDropDown, self).__init__(**kwargs)
        self.text = 'Material'


class ConstraintDropDown(DropDownButton):
    def __init__(self, **kwargs):

        kwargs['module'] = 'kivy.uix.togglebutton'
        kwargs['widget'] = 'ToggleButton'
        super(ConstraintDropDown, self).__init__(**kwargs)
        self.text = 'Constraints'


class LoadDropDown(DropDownButton):
    def __init__(self, **kwargs):

        kwargs['module'] = 'kivy.uix.togglebutton'
        kwargs['widget'] = 'ToggleButton'
        super(LoadDropDown, self).__init__(**kwargs)
        self.text = 'Loads'


class SolnProcDropDown(DropDownButton):
    def __init__(self, **kwargs):
        self.clss = inspect.getmembers(fea.FESolnProc, inspect.isclass)
        self.cll_name = []
        self.text = 'Solution Type'
        for index in range(len(self.clss)):
            self.cll_name.append(self.clss[index][0])
        kwargs['type'] = self.cll_name
        kwargs['module'] = 'kivy.uix.button'
        kwargs['widget'] = 'Button'
        super(SolnProcDropDown, self).__init__(**kwargs)
        self.drop_list.bind(on_select = self.drop_select)

        self.selection = None

    def drop_select(self, *args):
        pos = self.cll_name.index(args[1])
        mat_list = self.clss[pos][1].material_list
        material_drop = self.parent.dropMat
        material_drop.drop_list.clear_widgets()

        mod = __import__('kivy.uix.button', fromlist=['Button'])
        widget_name = 'Button'
        attr = getattr(mod, widget_name)

        for i in mat_list:

            btn = attr(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: material_drop.drop_list.select(btn.text))
            material_drop.drop_list.add_widget(btn)

        material_drop.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))
