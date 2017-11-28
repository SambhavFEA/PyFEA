import abc
from fea.FEStiffness.FEStiffness import FEStiffness
from fea.FEShapeFunction.FESFIsoParaQuadElement import FEIsoParaQuadElement
from fea.Integration.GaussLegendreQuadrature import GaussLegendreQuadrature
import numpy as np


class FEPlaneStress(FEStiffness):
    material = np.array([])

    def __init__(self, *args, **kwargs):
        self.material = args[0]
        self.shape_function = FEIsoParaQuadElement(kwargs['coords'][0], kwargs['coords'][1], kwargs['coords'][2], kwargs['coords'][3])

    def get_element_stiffness_matrix(self):
        h = self.material[2]

        #ke = dblquad(lambda s, t: self.integrand(s, t), -1.0, 1.0, lambda x:-1.0, lambda x: 1.0)
        ke = GaussLegendreQuadrature.dblintegration(self.integrand, 2)

        # k = [
        #     [1. / 2. - mu / 6., - mu / 8. - 1. / 8., mu / 6., (3. * mu) / 8. - 1. / 8., mu / 12. - 1. / 4., mu / 8. + 1. / 8.,
        #      - mu / 12. - 1. / 4., 1. / 8. - (3. * mu) / 8.],
        #     [- mu / 8. - 1. / 8., 1. / 2. - mu / 6., 1. / 8. - (3. * mu) / 8., - mu / 12. - 1. / 4., mu / 8. + 1. / 8., mu / 12. - 1. / 4.,
        #      (3. * mu) / 8. - 1. / 8., mu / 6.],
        #     [mu / 6., 1. / 8. - (3. * mu) / 8., 1. / 2. - mu / 6., mu / 8. + 1. / 8., - mu / 12. - 1. / 4., (3. * mu) / 8. - 1. / 8.,
        #      mu / 12. - 1. / 4., - mu / 8. - 1. / 8.],
        #     [(3. * mu) / 8. - 1. / 8., - mu / 12. - 1. / 4., mu / 8. + 1. / 8., 1. / 2. - mu / 6., 1. / 8. - (3. * mu) / 8., mu / 6.,
        #      - mu / 8. - 1. / 8., mu / 12. - 1. / 4.],
        #     [mu / 12. - 1. / 4., mu / 8. + 1. / 8., - mu / 12. - 1. / 4., 1. / 8. - (3. * mu) / 8., 1. / 2. - mu / 6., - mu / 8. - 1. / 8.,
        #      mu / 6., (3. * mu) / 8. - 1. / 8.],
        #     [mu / 8. + 1. / 8., mu / 12. - 1. / 4., (3. * mu) / 8. - 1. / 8., mu / 6., - mu / 8. - 1. / 8., 1. / 2. - mu / 6.,
        #      1. / 8. - (3. * mu) / 8., - mu / 12. - 1. / 4.],
        #     [- mu / 12. - 1. / 4., (3. * mu) / 8. - 1. / 8., mu / 12. - 1. / 4., - mu / 8. - 1. / 8., mu / 6., 1. / 8. - (3. * mu) / 8.,
        #      1. / 2. - mu / 6., mu / 8. + 1. / 8.],
        #     [1. / 8. - (3. * mu) / 8., mu / 6., - mu / 8. - 1. / 8., mu / 12. - 1. / 4., (3. * mu) / 8. - 1. / 8., - mu / 12. - 1. / 4.,
        #      mu / 8. + 1. / 8., 1. / 2. - mu / 6.]]
        #
        # ke = h * (E / (1. - mu**2.)) * np.array(k)

        return ke

    def integrand(self, s, t):
        E = self.material[0]
        mu = self.material[1]

        C = E * np.array([[1, mu, 0], [mu, 1, 0], [0, 0, (1 - mu) / 2]]) / (1 - mu ** 2)

        B = self.shape_function.get_b_matrix(s, t)

        return np.linalg.det(self.shape_function.get_jacobian(s, t)) * np.matmul(B.transpose(), np.matmul(C, B))
