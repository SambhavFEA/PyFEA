import numpy as np


class FEModel(object):
    ele = np.array([[], [4]])  # ele[element no, node no]   ---- ele[n,4] size
    nodes = np.array([[], [2]])  # nodes[node no, coordinates]  ----- nodes[n,2] size
    material = np.array([])
    forces = np.array([[], []])  # forces[forceno,[node number, forcex, forcey]
    boundary_constraints = np.array([[], []])  # constraints[constraint no,[node number, dof,val]]

    kStif = np.zeros([], [])
    uDisp = np.zeros([])
    fForce = np.zeros([])

    ndof = 2
    nnpe = 4

    def __init__(self, elements, nodes, material, forces, fixtures):
        # input must be elements, nodes and materials
        ele = elements
        self.nodes = nodes
        self.material = material
        self.forces = forces
        constraints = fixtures

        nodesSize = np.shape(nodes)

        kStif = np.zeros((nodesSize[0] * self.ndof, nodesSize[0] * self.ndof))
        uDisp = np.zeros(nodesSize[0] * self.ndof)
        fForce = np.zeros(nodesSize[0] * self.ndof)
        return

    def __init__(self, filename):
        self.read_input_2D(filename)

    def read_input_2D(self,filename):

        f = open(filename, 'r')
        lines = f.readlines()

        # Node Coordinate Matrix
        num_node_coord = int(lines[2])
        self.nodes = np.zeros([num_node_coord, 2])
        for i in range(num_node_coord):
            self.nodes[i] = list(map(float, lines[2 + i + 1].split(" ")))

        # Connectivity Matrix
        num_elem = int(lines[7 + num_node_coord][0])
        # Dynamic nnpe (nnpe stays const)
        nnpe = np.shape((list(map(int, lines[8 + num_node_coord].split(" ")))))[0]

        self.ele = np.zeros((num_elem, nnpe))
        for j in range(num_elem):
            self.ele[j] = list(map(int, lines[7 + num_node_coord + j + 1].split(" ")))

        # Material Properties
        num_of_mat_prop = int(lines[
                                  11 + num_node_coord + num_elem])  # Hash Mapping can be used for different type of material properties. Dummy!
        self.material = np.zeros([num_of_mat_prop, 1])
        for k in range(num_of_mat_prop):
            self.material[k] = float(lines[11 + num_node_coord + num_elem + k + 1])

        # Boundary Constraint
        num_of_bc = int(lines[15 + num_node_coord + num_elem + num_of_mat_prop])
        self.boundary_constraints = np.zeros([num_of_bc, 3])
        for l in range(num_of_bc):
            self.boundary_constraints[l] = list(
                map(float, lines[15 + num_node_coord + num_elem + num_of_mat_prop + l + 1].split(" ")))

        # Force Constraint
        num_of_fc = int(lines[19 + num_node_coord + num_elem + num_of_mat_prop + num_of_bc])
        self.forces = np.zeros([num_of_fc, 3])
        for m in range(num_of_fc):
            self.forces[m] = list(
                map(float, lines[19 + num_node_coord + num_elem + num_of_mat_prop + num_of_bc + m + 1].split(" ")))



    def bottomleftnode(self,element_no): #return the node number of bottom left node.  Maybe unnecessary.

        pass


def main():
    return
