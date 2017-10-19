import fileI_O
import globalStiffAssem
from fea.FESolvers.FESolve import FELuDecompSolve

if __name__ == '__main__':
    #Mod = FEModel.FEModel('2DMeshTest.sam')
    #assemble_global_stiffness(Mod)
    #apply_constraints(Mod)
    #solveFEModel(Mod)
    #filename = 'test'
    #saveFEModel(filename,Mod)
    fileI = fileI_O.fileI_O('2DMeshTest.sam')

    globalStiffAssem.globalStiffAssem.assemble_global_stiffness(fileI.femodel)
    #print fileI.femodel.kStif
    print fileI.femodel.material.get_element_stiffness_matrix(0)
    globalStiffAssem.globalStiffAssem.apply_constraints(fileI.femodel)

    solver = FELuDecompSolve(fileI.femodel)

    print solver.finalArray



    pass

