import FEModel
import numpy as np
from assemble_global_stiffness import assemble_global_stiffness

if __name__ == '__main__':
    Mod = FEModel.FEModel('2DMeshTest.sam')
    assemble_global_stiffness(Mod)
    print Mod.global_stiffness
    pass

