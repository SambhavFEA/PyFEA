import abc
from fea.FEMaterial.FEMaterial import FEMaterial
import numpy as np


class FEPlaneStress(FEMaterial):
    material = np.array([])

    def __init__(self, *args):
        self.material = args[0]

    def get_element_stiffness_matrix(self, i):
        E = self.material[0][i]
        mu = self.material[1][i]
        h = self.material[2][i]

        k = [
            [1 / 2 - (2 * mu) / 3, -1 / 8, mu / 6, mu / 2 - 1 / 8, mu / 3 - 1 / 4, 1 / 8, mu / 6 - 1 / 4,
             1 / 8 - mu / 2]
            [-1 / 8, 1 / 2 - (
            2 * mu) / 3, 1 / 8 - mu / 2, mu / 6 - 1 / 4, 1 / 8, mu / 3 - 1 / 4, mu / 2 - 1 / 8, mu / 6]
            [mu / 6, 1 / 8 - mu / 2, 1 / 2 - (
            2 * mu) / 3, 1 / 8, mu / 6 - 1 / 4, mu / 2 - 1 / 8, mu / 3 - 1 / 4, -1 / 8]
            [mu / 2 - 1 / 8, mu / 6 - 1 / 4, 1 / 8, 1 / 2 - (
            2 * mu) / 3, 1 / 8 - mu / 2, mu / 6, -1 / 8, mu / 3 - 1 / 4]
            [mu / 3 - 1 / 4, 1 / 8, mu / 6 - 1 / 4, 1 / 8 - mu / 2, 1 / 2 - (
            2 * mu) / 3, -1 / 8, mu / 6, mu / 2 - 1 / 8]
            [1 / 8, mu / 3 - 1 / 4, mu / 2 - 1 / 8, mu / 6, -1 / 8, 1 / 2 - (
            2 * mu) / 3, 1 / 8 - mu / 2, mu / 6 - 1 / 4]
            [mu / 6 - 1 / 4, mu / 2 - 1 / 8, mu / 3 - 1 / 4, -1 / 8, mu / 6, 1 / 8 - mu / 2, 1 / 2 - (
            2 * mu) / 3, 1 / 8]
            [1 / 8 - mu / 2, mu / 6, -1 / 8, mu / 3 - 1 / 4, mu / 2 - 1 / 8, mu / 6 - 1 / 4, 1 / 8, 1 / 2 - (
            2 * mu) / 3]]

        ke = h * (E / (1 - mu ^ 2)) * np.array(k)

        return ke
