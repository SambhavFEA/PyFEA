import numpy as np
import FEModel

def solveFEModel(model = FEModel.FEModel):

    model.disp_result = np.matmul(model.fForce,np.linalg.inv(model.global_stiffness))

def resultantNodes (model = FEModel.FEModel):

    tempArray = model.disp_result.reshape(6,2)
    finalArray =  np.zeros(len(tempArray))
    for i in model.nodes:
        finalArray[i] = model.nodes[i] + tempArray[i]

    return finalArray
