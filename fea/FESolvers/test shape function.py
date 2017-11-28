from fea.FEStiffness.FEPlaneStress import FEPlaneStress

mat = [200000, 0.33, 1]
pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
kwargs = {'coords': pts}

kstiff = FEPlaneStress(mat, **kwargs)

print(kstiff.get_element_stiffness_matrix())
