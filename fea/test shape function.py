from fea.FEStiffness.FEPlaneStress import FEPlaneStress2D
from fea.FEMass.FEVarMassLumping import FEVarMassLumping2D

mat = [200000, 0.33, 1]
mat2 = [1, 10000]
pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
kwargs = {'coords': pts}

kstiff = FEPlaneStress2D(mat, **kwargs)

me = FEVarMassLumping2D(mat2, **kwargs)

print(kstiff.get_element_stiffness_matrix())
print(me.get_mass_matrix())
