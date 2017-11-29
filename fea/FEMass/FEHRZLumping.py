from fea.Integration.GaussLegendreQuadrature import GaussLegendreQuadrature
from fea.FEMass.FEVarMassLumping import FEVarMassLumping2D
import numpy as np


class FEHRZLumping2D(FEVarMassLumping2D):

    def get_mass_matrix(self):
        h = self.material[0]
        density = self.material[1]
        me = h * density * GaussLegendreQuadrature.dblintegration(lambda s, t: self.integrand(s, t).diagonal(), 2)
        trace = np.sum(me, dtype=np.float)
        me = me/trace
        return np.diag(me)
