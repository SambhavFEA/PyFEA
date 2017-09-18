import numpy as np

from fea.FEMaterial.FEMaterial import FEMaterial


class FEModel(object):
 # ele[element no, node no]   ---- ele[n,4] size
 # nodes[node no, coordinates]  ----- nodes[n,2] size
 # material[material propert 1, material property 2, .....]
 # forces[forceno,[node number, forcex, forcey]
 # constraints[constraint no,[node number, dof,val]]

    ndof = 2
    nnpe = 4

    def __init__(self, *args):

        self.fe_model(args[0], args[1], args[2], args[3], args[4])

    def fe_model(self, elements, nodes, material, forces, fixtures):
        # input must be elements, nodes and materials
        self.ele = elements
        self.nodes = nodes
        self.material = material
        self.forces = forces
        self.boundary_constraints = fixtures

        nodesSize = np.shape(nodes)

        self.kStif = np.zeros((nodesSize[0] * self.ndof, nodesSize[0] * self.ndof))
        self.uDisp = np.zeros(nodesSize[0] * self.ndof)
        self.fForce = np.zeros(nodesSize[0] * self.ndof)
        return


