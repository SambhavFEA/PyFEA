# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:08:23 2017

@author: Apoorv
"""
import numpy as np

def read_fea_input(self, filename):
    
    #Initializing
    NodeX = []
    NodeY = []
    Elem = []
    Material = []
    bc = []
    ff =[]
    
    f = open(filename,'r')
    lines = f.readlines()
    
    #Node Coordinate Matrix
    num_node_coord = int(lines[2][0])
    
    for i in range(num_node_coord):
        NodeX[i] = float(lines[2+i][2:5])
        NodeY[i] = float(lines[2+i][6:9])
    
    #Connectivity Matrix
    num_elem = int(lines[7+num_node_coord][0]) 
    
    for j in range(num_elem):
        Elem[j] = list(map(int,lines[7+num_node_coord+j].split()))
        
    #Material Properties
    num_of_mat_prop = int(lines[11+num_node_coord+num_elem])
    for k in range(num_of_mat_prop):
        Material[k] = int(lines[11+num_node_coord+num_elem+k])

    #Boundary Constraint
    num_of_bc = int(lines[15+num_node_coord+num_elem+num_of_mat_prop])
    for l in range(num_of_bc):
        bc[l] = list(map(int,lines[15+num_node_coord+num_elem+num_of_mat_prop+l]))
        
    #Force Constraint
    num_of_fc = int(lines[19+num_node_coord+num_elem+num_of_mat_prop+num_of_bc])
    for m in range(num_of_fc):
        ff[m] = list(map(int,lines[19+num_node_coord+num_elem+num_of_mat_prop+num_of_bc+m]))
        
    
    