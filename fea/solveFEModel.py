import numpy as np
import FEModel

def solveFEModel(model = FEModel.FEModel):

    model.uDisp = np.matmul(model.fForce,np.linalg.inv(model.kStif))

def resultantNodes (model = FEModel.FEModel):

    tempArray = model.uDisp.reshape(6,2)
    finalArray =  np.zeros(len(tempArray))
    for i in model.nodes:
        finalArray[i] = model.nodes[i] + tempArray[i]

    return finalArray
