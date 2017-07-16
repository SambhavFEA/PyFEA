import FEModel
import numpy as np
from assemble_global_stiffness import assemble_global_stiffness
from apply_constraints import apply_constraints
if __name__ == '__main__':
    Mod = FEModel.FEModel('2DMeshTest.sam')
    assemble_global_stiffness(Mod)
    #print Mod.global_stiffness
    apply_constraints(Mod)
    print Mod.uDisp
    pass

