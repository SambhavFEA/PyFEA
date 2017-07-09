# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:30:41 2017

@author: Apoorv
Purpose - Return assembled global stiffness matrix 
        - The material is assumed to be isotropic
        - All the nodes are assumed to have same degree of freedom
        - Elem Connectivity Follows GID mesh rules
"""
import numpy as np
import FEModel

def assemble_global_stiffness(model = FEModel.FEModel):
    num_of_elem = getNumOfElem(model)
    num_of_nodes_elem = getNumOfNodes(model)
    dof_node = getDof(model)
    model.kStif = elem_stiff(model)
    model.global_stiffness = np.zeros((num_of_elem*dof_node,num_of_elem*dof_node))


    for elem_num in range(num_of_elem):
        for a in range(num_of_nodes_elem):
            for i in range(dof_node):
                for b in range(num_of_nodes_elem):
                    for j in range(dof_node):
                        row = dof_node*(int(model.ele[elem_num, a])) + i    # Not sure how elem_connectivity table will look like
                        col = dof_node*(int(model.ele[elem_num, b])) + j
                        model.global_stiffness[row,col] = model.global_stiffness[row,col] + model.kStif[(dof_node * a) + i, (dof_node * b) + j]  # Cross-check the valus of elem_stiffness corresponding to global position



def getNumOfElem(model = FEModel.FEModel):
    return len(model.ele)

def getNumOfNodes(model = FEModel.FEModel):
    return (len(model.nodes))

def getDof(data):
    return 2    #Finalize on how to decide degree of freedom


def elem_stiff(model=FEModel.FEModel):
    E = model.material[0][0]
    nu = model.material[1][0]

    k = np.multiply((E/((1+nu)*(1-2*nu))),
         [[1-nu, nu, nu, 0., 0., 0.],
         [nu, 1-nu, nu, 0., 0., 0.],
         [nu, nu, 1-nu, 0., 0., 0.],
         [0., 0., 0., 1-(2*nu), 0., 0.],
         [0., 0., 0., 0., 1-(2*nu), 0.],
         [0., 0., 0., 0., 0., 1-(2*nu)]])
    return k
# Changes
def apoorvname():
    return "Apoorv Garg"
                
def amishname():
    return "Amish Gadigi"