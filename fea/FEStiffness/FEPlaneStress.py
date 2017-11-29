from fea.FEStiffness.FEStiffness import FEStiffness
import numpy as np


class FEPlaneStress2D(FEStiffness):
    material = np.array([])

    def get_C(self):
        E = self.material[0]
        mu = self.material[1]
        return E * np.array([[1., mu, 0.], [mu, 1., 0.], [0., 0., (1. - mu) / 2.]]) / (1. - mu ** 2)

