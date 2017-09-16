import numpy as np
import FEModel
class fileI_O(object):

    def __init__(self, filename):
        self.FEModel = FEModel.FEModel (filename)
        self.path = filename

    def saveFEModel(self, fileName ):
        file1 = open(fileName + '.sam', "w")

        # Node Coordinate
        file1.write('#Node Coordinate\n')
        file1.write('X  Y\n')
        file1.write(str(len(self.nodes)) + '\n')
        for i in self.nodes:
            file1.write(str(i) + '\n')
        file1.write(" ")

        # Connectivity Table
        file1.write("#Connectivity Matrix\n")
        file1.write("Element    Node1   Node2	Node3	Node4\n")
        file1.write(str(len(self.ele)) + "\n")
        for i1 in self.ele:
            file1.write(str(i1) + "\n")
        file1.write(" ")

        # Material Properties
        file1.write("#Material Properties\n")
        file1.write("E  Poisson`s Ratio\n")
        file1.write(str(len(self.material)) + "\n")
        for i2 in self.material:
            file1.write(str(i2) + "\n")
        file1.write(" ")

        # Boundary Condition
        file1.write("#Boundary Condition\n")
        file1.write("Node    DOF     Value\n")
        file1.write(str(len(self.boundary_constraints)) + "\n")
        for i3 in self.boundary_constraints:
            file1.write(str(i3) + "\n")
        file1.write(" ")

        # Force Constraint
        file1.write("#Force\n")
        file1.write("Node   Fx  Fy\n")
        file1.write(str(len(self.forces)) + "\n")
        for i4 in self.forces:
            file1.write(str(i4) + "\n")

        file1.close()