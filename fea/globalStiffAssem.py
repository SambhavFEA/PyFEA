import FEModel
import numpy as np


class globalStiffAssem(object):
    @staticmethod
    def getNumOfElem(model=FEModel.FEModel):
        return len(model.ele)

    @staticmethod
    def getNumOfNodes(model=FEModel.FEModel):
        return (len(model.ele[0]))  # Number of nodes per element is constant

    @staticmethod
    def getTotalNodes(model=FEModel.FEModel):
        return len(model.nodes)

    @staticmethod
    def getDof(data):
        return 2  # Finalize on how to decide degree of freedom

    @staticmethod
    def assemble_global_stiffness(model=FEModel.FEModel):
        num_of_elem = len(model.ele)
        num_of_nodes_elem = (len(model.ele[0]))
        total_num_of_nodes = len(model.nodes)
        dof_node = 2
        element_kStif = model.material.get_element_stiffness_matrix(0)
        model.kStif = np.zeros((total_num_of_nodes * dof_node, total_num_of_nodes * dof_node))

        for elem_num in range(num_of_elem):
            for a in range(num_of_nodes_elem):
                for i in range(dof_node):
                    for b in range(num_of_nodes_elem):
                        for j in range(dof_node):
                            row = dof_node * (int(model.ele[elem_num, a])) + i
                            col = dof_node * (int(model.ele[elem_num, b])) + j
                            ele_row = (dof_node * a) + i
                            ele_col = (dof_node * b) + j
                            model.kStif[row, col] = model.kStif[row, col] + element_kStif[ele_row, ele_col]

    @staticmethod
    def apply_constraints(model=FEModel.FEModel):

        ndof = getattr(model, 'ndof')
        nnpe = getattr(model, 'nnpe')
        num_of_nodes = len(getattr(model, 'nodes'))

        positions = []

        forces = getattr(model, 'forces')
        forces_size = np.shape(forces)
        ff = getattr(model, 'fForce')

        for i in range(forces_size[0]):
            node_num = int(forces[i, 0])
            ff[node_num * ndof] = forces[i, 1]
            ff[(node_num * ndof) + 1] = forces[i, 2]

        # setattr(model, 'fForce', ff)

        displacement = getattr(model, 'boundary_constraints')
        disp_size = np.shape(displacement)
        dd = getattr(model, 'uDisp')

        for i in range(disp_size[0]):
            node_num = int(displacement[i, 0])
            dd[(node_num * ndof) + int(displacement[i, 1])] = displacement[i, 2]
            if displacement[i, 2] == 0.:
                positions.append(int((displacement[i, 0] * ndof) + displacement[
                    i, 1]))  # Append command not working. Positions is still an empty array

        kstiff = getattr(model, 'kStif')
        posit = np.array(positions)
        kstiff = np.delete(kstiff, positions, axis=0)
        kstiff = np.delete(kstiff, positions, axis=1)

        dd = np.delete(dd, positions, axis=0)
        ff = np.delete(ff, positions, axis=0)

        setattr(model, 'uDisp', dd)
        setattr(model, 'kStif', kstiff)
        setattr(model, 'fForce', ff)
        setattr(model, 'positions', posit)
        return
