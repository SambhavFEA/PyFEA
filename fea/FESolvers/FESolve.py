import numpy as np

from fea.FEModel import FELinearModel


class FELuDecompSolve(object):

    def __init__(self, model= FELinearModel.FEModel):
        full_disp = np.zeros(len(model.uDisp) + len(model.positions))
        model.uDisp = np.matmul(model.fForce,np.linalg.inv(model.kStif))
        self.finalArray = np.zeros(len(full_disp))

        #Get new nodes value here


        #initialize
        j=0
        k=0
        for i in range(len(full_disp)):
            if j < len(model.positions):

                if i != model.positions[j]:
                    self.finalArray[i] = model.uDisp[k]
                    k = k +1
                else:
                    self.finalArray[i] = model.boundary_constraints[j][2]
                    j = j+1
            else:
                self.finalArray[i] = model.uDisp[k]
                k = k + 1



        #tempArray = np.array(FELuDecompSolve.solDisp.reshape(4, 2))
        #finalArray = np.zeros(len(tempArray))
        #for i in range(len(model.nodes)):
        #    finalArray[i] = model.nodes[i] + tempArray[i]

        #FELuDecompSolve.resNodes = finalArray


