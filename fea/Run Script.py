import FEModel
import numpy as np
import fileI_O
import globalStiffAssem
from FESolve import FeLuDecompSolve

import globalStiffAssem
from solveFEModel import solveFEModel

if __name__ == '__main__':
    #Mod = FEModel.FEModel('2DMeshTest.sam')
    #assemble_global_stiffness(Mod)
    #apply_constraints(Mod)
    #solveFEModel(Mod)
    #filename = 'test'
    #saveFEModel(filename,Mod)
    fileI = fileI_O.fileI_O('2DMeshTest.sam')

    globalStiffAssem.globalStiffAssem.assemble_global_stiffness(fileI.FEModel)
    globalStiffAssem.globalStiffAssem.apply_constraints(fileI.FEModel)

    solver = FeLuDecompSolve(fileI.FEModel)

    #print Mod.uDisp
    pass

