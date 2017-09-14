import numpy as np
import FEModel

def saveFEModel(fileName,model = FEModel.FEModel):
    file1 = open(fileName+'.sam', "w")

    #Node Coordinate
    file1.write('#Node Coordinate\n')
    file1.write('X  Y\n')
    file1.write(str(len(model.nodes))+'\n')
    for i in model.nodes:
        file1.write(str(i)+'\n')
    file1.write(" ")

    #Connectivity Table
    file1.write("#Connectivity Matrix\n")
    file1.write("Element    Node1   Node2	Node3	Node4\n")
    file1.write(str(len(model.ele))+"\n")
    for i1 in model.ele:
        file1.write(str(i1)+"\n")
    file1.write(" ")

    #Material Properties
    file1.write("#Material Properties\n")
    file1.write("E  Poisson`s Ratio\n")
    file1.write(str(len(model.material))+"\n")
    for i2 in model.material:
        file1.write(str(i2)+"\n")
    file1.write(" ")

    #Boundary Condition
    file1.write("#Boundary Condition\n")
    file1.write("Node    DOF     Value\n")
    file1.write(str(len(model.boundary_constraints))+"\n")
    for i3 in model.boundary_constraints:
        file1.write(str(i3)+"\n")
    file1.write(" ")

    #Force Constraint
    file1.write("#Force\n")
    file1.write("Node   Fx  Fy\n")
    file1.write(str(len(model.forces))+"\n")
    for i4 in model.forces:
        file1.write(str(i4)+"\n")

    file1.close()



