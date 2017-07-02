
import numpy as np

class Model:

    ele = np.array([[],[4]])                #ele[element no, node no]   ---- ele[n,4] size
    nodes = np.array([[],[2]])              #nodes[node no, coordinates]  ----- nodes[n,2] size
    material = np.array([])
    forces = np.array([],[3])               #forces[forceno,[node number, forcex, forcey]
    constraints = np.array([],[3])          #constraints[constraint no,[node number, dof,val]]

    kStif = np.zeros([],[])
    uDisp = np.zeros([])
    fForce = np.zeros([])

    ndof = 2
    nnpe = 4

    def _init_(self,elements,nodes,material,forces,fixtures):
        #input must be elements, nodes and materials
        ele=elements
        self.nodes = nodes
        self.material = material
        self.forces = forces
        constraints = fixtures

        nodesSize = np.shape(nodes)

        kStif = np.zeros((nodesSize(0)*self.ndof,nodesSize(0)*self.ndof))
        uDisp = np.zeros(nodesSize(0)*self.ndof)
        fForce = np.zeros(nodesSize(0)*self.ndof)
        return

def readInput():
 return


def main():

 return