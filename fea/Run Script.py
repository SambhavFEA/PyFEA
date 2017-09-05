import FEModel
import numpy as np

from assemble_global_stiffness import assemble_global_stiffness
from apply_constraints import apply_constraints
from solveFEModel import solveFEModel
from saveFEModel import saveFEModel
if __name__ == '__main__':
    Mod = FEModel.FEModel('2DMeshTest.sam')
    assemble_global_stiffness(Mod)
    apply_constraints(Mod)
    solveFEModel(Mod)
    filename = 'test'
    saveFEModel(filename,Mod)
    print Mod.disp_result
    pass

