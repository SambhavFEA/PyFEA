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
import FEModel as Model

def assemble_global_stiffness(Model):
    num_of_elem = getNumOfElem(Model.ele)
    num_of_nodes_elem = getNumOfNodes(Model)
    dof_node = getDof(Model)
    global_stiffness = []

    for elem_num in num_of_elem:
        for a in num_of_nodes_elem:
            for i in dof_node:
                for b in num_of_nodes_elem:
                    for j in dof_node:
                        row = dof_node*(Model.ele(elem_num,a+1))+i    # Not sure how elem_connectivity table will look like
                        col = dof_node*(Model.ele(elem_num,b+1))+j
                        global_stiffness[row,col] = global_stiffness[row,col] + Model.kStif[(dof_node*a)+i,(dof_node*b)+j]  # Cross-check the valus of elem_stiffness corresponding to global position
    
    return global_stiffness

def getNumOfElem(Model):
    return len(Model.ele)

def getNumOfNodes(Model):
    return (len(Model.nodes))

def getDof(data):
    return 2    #Finalize on how to decide degree of freedom

# Changes
def apoorvname():
    return "Apoorv Garg"
                
def amishname():
    return "Amish Gadigi"