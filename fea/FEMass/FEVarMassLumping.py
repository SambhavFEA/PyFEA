from fea.FEShapeFunction.FESFIsoParaQuadElement import FEIsoParaQuadElement
from fea.Integration.GaussLegendreQuadrature import GaussLegendreQuadrature
import numpy as np


class FEVarMassLumping2D(object):
    """
    This class is used to create Variational Mass Lumping Matrix for 2D element. After creating an instance of this class,
    call get_mass_matrix to generate the mass matrix. The same function will return the mass matrix too.
    """

    def __init__(self, *args, **kwargs):
        """
        This class is used to create Variational Mass Lumping Matrix for a 2D element.
        :param args: Only one input is required for args. It needs to be a list of element thickness and density respectively
        :param kwargs: kwargs must be a list of four tuples with key 'coords' e.g. 'coords': [(1,2), (3,4), (5,6), (7,8)]
        """
        self.material = args[0]
        self.shape_function = FEIsoParaQuadElement(kwargs['coords'])

    def get_mass_matrix(self):
        h = self.material[0]
        density = self.material[1]
        me = h * density * GaussLegendreQuadrature.dblintegration(self.integrand, 2)
        return me

    def integrand(self, s, t):
        n = np.array(self.shape_function.get_n(s, t))
        return np.linalg.det(self.shape_function.get_jacobian(s, t)) * np.matmul(n.transpose(), n)
