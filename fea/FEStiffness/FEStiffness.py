import abc
import numpy as np
from fea.Integration.GaussLegendreQuadrature import GaussLegendreQuadrature
from fea.FEShapeFunction.FESFIsoParaQuadElement import FEIsoParaQuadElement


class FEStiffness(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.material = args[0]
        self.shape_function = FEIsoParaQuadElement(kwargs['coords'])

    def get_element_stiffness_matrix(self):
        h = self.material[2]
        ke = h * GaussLegendreQuadrature.dblintegration(self.integrand, 2)
        return ke

    def integrand(self, s, t):
        C = self.get_C()
        B = self.shape_function.get_b_matrix(s, t)
        return np.linalg.det(self.shape_function.get_jacobian(s, t)) * np.matmul(B.transpose(), np.matmul(C, B))
