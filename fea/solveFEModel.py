import numpy as np
import FEModel

def solveFEModel(model = FEModel.FEModel):
    size_disp = len(model.fForce)
    model.disp_result = np.array([size_disp])
    model.disp_result = np.divide(model.fForce,model.global_stiffness)
