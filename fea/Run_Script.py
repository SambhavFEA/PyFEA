import Model
import numpy as np
filename = '2DMeshTest.sam'
if __name__ == '__main__':

    Mod = Model.Model(filename)
    print Mod.nodes
