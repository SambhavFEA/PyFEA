import FEModel
import numpy as np

if __name__ == '__main__':
    Mod = FEModel.FEModel('2DMeshTest.sam')
    print Mod.material

