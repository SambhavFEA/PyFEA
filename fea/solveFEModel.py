import numpy as np
import FEModel

def solveFEModel(model = FEModel.FEModel):

    model.disp_result = np.matmul(model.fForce,np.linalg.inv(model.global_stiffness))
