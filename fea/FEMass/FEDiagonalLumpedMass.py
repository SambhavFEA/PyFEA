from fea.FEShapeFunction.FESFIsoParaQuadElement import FEIsoParaQuadElement
import numpy as np


class FEDiagonalLumpedMass2D(object):

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
        pts = self.shape_function.get_all_pts()
        area = self.shape_function.get_area()
        me = ((density * area * h) * np.identity(self.shape_function.ndof)) / self.shape_function.num_of_nodes
        return me
