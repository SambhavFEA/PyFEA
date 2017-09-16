import FEModel
import numpy as np
import fileI_O

from assemble_global_stiffness import assemble_global_stiffness
from apply_constraints import apply_constraints
from solveFEModel import solveFEModel

if __name__ == '__main__':
    #Mod = FEModel.FEModel('2DMeshTest.sam')
    #assemble_global_stiffness(Mod)
    #apply_constraints(Mod)
    #solveFEModel(Mod)
    #filename = 'test'
    #saveFEModel(filename,Mod)
    fileI = fileI_O.fileI_O('2DMeshTest.sam')
    fileI.saveFEModel('fileI_Otest')

    #print Mod.uDisp
    pass

