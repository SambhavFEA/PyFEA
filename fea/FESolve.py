from globalStiffAssem import globalStiffAssem
import FEModel
import numpy as np

class FeLuDecompSolve(object):

    def __init__(self, model= FEModel.FEModel):
        FeLuDecompSolve.solDisp = np.matmul(model.fForce,np.linalg.inv(model.kStif))

        #Get new nodes value here
        tempArray = FeLuDecompSolve.solDisp.reshape(4, 2)
        finalArray = np.zeros(len(tempArray))
        for i in model.nodes:
            finalArray[i] = model.nodes[i] + tempArray[i]

        FeLuDecompSolve.resNodes = finalArray


