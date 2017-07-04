# -*- coding: utf-8 -*-
import numpy as np
#Initializing


def read_input_2D(self,filename):
    
    f = open(filename,'r')
    lines = f.readlines()
    
    #Node Coordinate Matrix
    num_node_coord = int(lines[2])
    Node = np.zeros([num_node_coord,2])    
    for i in range(num_node_coord):
        Node[i] = list(map(float,lines[2+i+1].split(" ")))
   
    #Connectivity Matrix
    num_elem = int(lines[7+num_node_coord][0]) 
    #Dynamic nnpe (nnpe stays const)
    nnpe = np.shape((list(map(int,lines[8+num_node_coord].split(" "))))[0])
    
    Elem = np.zeros([num_elem,nnpe]) 
    for j in range(num_elem):
        Elem[j] = list(map(int,lines[7+num_node_coord+j+1].split(" ")))
        
    #Material Properties
    num_of_mat_prop = int(lines[11+num_node_coord+num_elem])        #Hash Mapping can be used for different type of material properties. Dummy!
    Material = np.zeros([num_of_mat_prop,1])
    for k in range(num_of_mat_prop):
        Material[k] = int(lines[11+num_node_coord+num_elem+k+1])

    #Boundary Constraint
    num_of_bc = int(lines[15+num_node_coord+num_elem+num_of_mat_prop])
    bc = np.zeros([num_of_bc,3])
    for l in range(num_of_bc):
        bc[l] = list(map(float,lines[15+num_node_coord+num_elem+num_of_mat_prop+l+1].split(" ")))
        
    #Force Constraint
    num_of_fc = int(lines[19+num_node_coord+num_elem+num_of_mat_prop+num_of_bc])
    ff = np.zeros([num_of_fc,3])
    for m in range(num_of_fc):
        ff[m] = list(map(float,lines[19+num_node_coord+num_elem+num_of_mat_prop+num_of_bc+m+1].split(" ")))
    
    pass
    
read_input_2D("2DMeshTest.sam")