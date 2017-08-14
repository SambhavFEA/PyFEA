import numpy as np
import FEModel

def saveFEModel(model = FEModel.FEModel,fileName):
    file1 = open(fileName+'.sam', "w")

    #Node Coordinate
    file1.write('#Node Coordinate')
    file1.write('X  Y')
    file1.write(len(model.nodes))
    for i in model.nodes:
        file1.write(i)
    file1.write(" ")

    #Connectivity Table
    file1.write("#Connectivity Matrix")
    file1.write("Element    Node1   Node2	Node3	Node4")
    file1.write(len(model.ele))
    for i1 in model.ele:
        file1.write(i1)
    file1.write(" ")

    #Material Properties
    file1.write("#Material Properties")
    file1.write("E  Poisson`s Ratio")
    file1.write(len(model.material))
    for i2 in model.material:
        file1.write(i2)
    file1.write(" ")

    #Boundary Condition
    file1.write("#Boundary Condition")
    file1.write("Node    DOF     Value")
    file1.write(len(model.material))
    for i3 in model.material:
        file1.write(i3)
    file1.write(" ")

    #Force Constraint
    file1.write("#Force")
    file1.write("Node   Fx  Fy")
    file1.write(len(model.forces))
    for i4 in model.forces:
        file1.write(i4)

    file.close()



