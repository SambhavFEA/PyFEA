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


def assemble_global_stiffness(self,elm_stiff,elem_connectivity,data):
    num_of_elem = getNumOfElem(elem_connectivity)
    num_of_nodes_elem = getNumOfNodes(elem_connectivity)
    dof_node = getDof(data)
    global_stiffness = []

    for elem_num in num_of_elem:
        for a in num_of_nodes_elem:
            for i in dof_node:
                for b in num_of_nodes_elem:
                    for j in dof_node:
                        row = dof_node*(elem_connectivity(elem_num,a+1))+i    # Not sure how elem_connectivity table will look like
                        col = dof_node*(elem_connectivity(elem_num,b+1))+j
                        global_stiffness[row,col] = global_stiffness[row,col] + elm_stiff[(dof_node*a)+i,(dof_node*b)+j]  # Cross-check the valus of elem_stiffness corresponding to global position
    
    return global_stiffness

def getNumOfElem(self,connectivity):
    return len(connectivity)

def getNumOfNodes(self, connectivity):
    return (len(connectivity[0])-1)

def getDof(data):
    return 2    #Finalize on how to decide degree of freedom

# Changes
def apoorvname():
    return "Apoorv Garg"
                
def amishname():
    return "Amish Gadigi"