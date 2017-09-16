import numpy as np

class fileI_O(object):

    ndof = 2
    nnpe = 4

    def __init__(self, *args):
        if len(args) == 1:
            self.read_input_2D(args[0])
        else:
            self.fe_model(args[0], args[1], args[2], args[3], args[4])

    def fe_model(self, elements, nodes, material, forces, fixtures):
        # input must be elements, nodes and materials
        ele = elements
        self.nodes = nodes
        self.material = material
        self.forces = forces
        self.boundary_constraints = fixtures

        nodesSize = np.shape(nodes)

        self.kStif = np.zeros((nodesSize[0] * self.ndof, nodesSize[0] * self.ndof))
        self.uDisp = np.zeros(nodesSize[0] * self.ndof)
        self.fForce = np.zeros(nodesSize[0] * self.ndof)
        return

    def read_input_2D(self, filename):

        f = open(filename, 'r')
        lines = f.readlines()

        # Node Coordinate Matrix
        num_node_coord = int(lines[2])
        self.nodes = np.zeros([num_node_coord, 2])
        for i in range(num_node_coord):
            self.nodes[i] = list(map(float, lines[2 + i + 1].split(" ")))

        # Connectivity Matrix
        num_elem = int(lines[6 + num_node_coord][0])
        # Dynamic nnpe (nnpe stays const)
        nnpe = np.shape((list(map(int, lines[8 + num_node_coord].split(" ")))))[0]

        self.ele = np.zeros((num_elem, nnpe))
        for j in range(num_elem):
            self.ele[j] = list(map(int, lines[7 + num_node_coord + j].split(" ")))

        # Material Properties
        num_of_mat_prop = int(lines[
                                  10 + num_node_coord + num_elem])  # Hash Mapping can be used for different type of material properties. Dummy!
        self.material = np.zeros([num_of_mat_prop, 1])
        for k in range(num_of_mat_prop):
            self.material[k] = float(lines[10 + num_node_coord + num_elem + k + 1])

        # Boundary Constraint
        num_of_bc = int(lines[14 + num_node_coord + num_elem + num_of_mat_prop])
        self.boundary_constraints = np.zeros([num_of_bc, 3])
        for l in range(num_of_bc):
            self.boundary_constraints[l] = list(
                map(float, lines[14 + num_node_coord + num_elem + num_of_mat_prop + l + 1].split(" ")))

        # Force Constraint
        num_of_fc = int(lines[18 + num_node_coord + num_elem + num_of_mat_prop + num_of_bc])
        self.forces = np.zeros([num_of_fc, 3])
        for m in range(num_of_fc):
            self.forces[m] = list(
                map(float, lines[18 + num_node_coord + num_elem + num_of_mat_prop + num_of_bc + m + 1].split(" ")))

        # Variable X and F set up {KX = F}
        nodesSize = np.shape(self.nodes)
        self.uDisp = np.zeros(nodesSize[0] * self.ndof)
        self.fForce = np.zeros(nodesSize[0] * self.ndof)

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