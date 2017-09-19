from globalStiffAssem import globalStiffAssem
import FEModel
import numpy as np

class FeLuDecompSolve(object):

    def __init__(self, model= FEModel.FEModel):
        full_disp = np.zeros(len(model.uDisp) + len(model.positions))
        model.uDisp = np.matmul(model.fForce,np.linalg.inv(model.kStif))
        self.finalArray = np.zeros(len(full_disp))

        #Get new nodes value here


        #initialize
        j=0
        k=0
        for i in range(len(full_disp)):
            if i < len(model.positions):

                if i != model.positions[j]:
                    self.finalArray[i] = model.uDisp[k]
                    k = k +1
                else:
                    model.boundary_constraints[j][2]
                    j = j+1
            else:
                self.finalArray[i] = model.uDisp[k]
                k = k + 1



        #tempArray = np.array(FeLuDecompSolve.solDisp.reshape(4, 2))
        #finalArray = np.zeros(len(tempArray))
        #for i in range(len(model.nodes)):
        #    finalArray[i] = model.nodes[i] + tempArray[i]

        #FeLuDecompSolve.resNodes = finalArray


