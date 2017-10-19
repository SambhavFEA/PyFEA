import numpy as np

from fea.FEMaterial.FePlaneStress2 import FEPlaneStress2
from fea.FEModel.FELinearModel import FEModel


class fileI_O(object):


    def __init__(self, filename):

        f = open(filename, 'r')
        lines = f.readlines()

        # Node Coordinate Matrix
        num_node_coord = int(lines[2])
        nodes = np.zeros([num_node_coord, 2])
        for i in range(num_node_coord):
            nodes[i] = list(map(float, lines[2 + i + 1].split(" ")))

        # Connectivity Matrix
        num_elem = int(lines[6 + num_node_coord][0])
        # Dynamic nnpe (nnpe stays const)
        nnpe = np.shape((list(map(int, lines[8 + num_node_coord].split(" ")))))[0]

        ele = np.zeros((num_elem, nnpe))
        for j in range(num_elem):
            ele[j] = list(map(int, lines[7 + num_node_coord + j].split(" ")))

        # Material Properties
        num_of_mat_prop = int(lines[
                                  10 + num_node_coord + num_elem])  # Hash Mapping can be used for different type of material properties. Dummy!
        material = np.zeros([num_of_mat_prop, 1])
        for k in range(num_of_mat_prop):
            material[k] = float(lines[10 + num_node_coord + num_elem + k + 1])
        materialobj = FEPlaneStress2(material)

        # Boundary Constraint
        num_of_bc = int(lines[14 + num_node_coord + num_elem + num_of_mat_prop])
        boundary_constraints = np.zeros([num_of_bc, 3])
        for l in range(num_of_bc):
            boundary_constraints[l] = list(
                map(float, lines[14 + num_node_coord + num_elem + num_of_mat_prop + l + 1].split(" ")))

        # Force Constraint
        num_of_fc = int(lines[18 + num_node_coord + num_elem + num_of_mat_prop + num_of_bc])
        forces = np.zeros([num_of_fc, 3])
        for m in range(num_of_fc):
            forces[m] = list(
                map(float, lines[18 + num_node_coord + num_elem + num_of_mat_prop + num_of_bc + m + 1].split(" ")))

        self.femodel = FEModel(ele, nodes, materialobj, forces, boundary_constraints)

        self.path = filename

    def saveFEModel(self, fileName):
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
