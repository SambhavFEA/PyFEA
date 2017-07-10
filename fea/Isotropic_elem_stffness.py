import FEModel
import numpy as np

def elem_stiff(model = FEModel.FEModel):
    E = model.material[0]
    nu = model.material[1]

    model.k = (E/(1+nu)*(1-3*nu))* \
        [[1-nu, nu, nu, 0., 0., 0.],
         [nu, 1-nu, nu, 0., 0., 0.],
         [nu, nu, 1-nu, 0., 0., 0.],
         [0., 0., 0., 1-(2*nu), 0., 0.],
         [0., 0., 0., 0., 1-(2*nu), 0.],
         [0., 0., 0., 0., 0., 1-(2*nu)]]



