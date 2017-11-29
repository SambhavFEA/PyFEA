import abc
from fea.FEStiffness.FEStiffness import FEStiffness
from fea.FEShapeFunction.FESFIsoParaQuadElement import FEIsoParaQuadElement
from fea.Integration.GaussLegendreQuadrature import GaussLegendreQuadrature
import numpy as np


class FEPlaneStrain2D(FEStiffness):

    def get_C(self):
        E = self.material[0]
        mu = self.material[1]
        return E * np.array([[1 - mu, mu, 0.], [mu, 1. - mu, 0.], [0., 0., 0.5 - mu]]) / ((1. + mu) * (1. - (2. * mu)))
