import math

import numpy as np
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget


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
