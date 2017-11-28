import abc


class FEMaterial(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_element_stiffness_matrix(self, i):
        pass
