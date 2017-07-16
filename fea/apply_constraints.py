import numpy as np
import FEModel


def apply_constraints(model = FEModel.FEModel):

    ndof = getattr(model, 'ndof')
    nnpe = getattr(model, 'nnpe')
    num_of_nodes = len(getattr(model, 'nodes'))

    model.positions = np.array([])

    forces = getattr(model, 'forces')
    forces_size = np.shape(forces)
    ff = getattr(model, 'fForce')

    for i in range(forces_size[0]):
        node_num = int(forces[i, 0])
        ff[(node_num-1) * ndof] = forces[i, 1]
        ff[((node_num-1) * ndof) + 1] = forces[i, 2]

    setattr(model, 'fForce', ff)

    displacement = getattr(model, 'boundary_constraints')
    disp_size = np.shape(displacement)
    dd = getattr(model, 'uDisp')

    for i in range(disp_size[0]):
        node_num = int(displacement[i, 0])
        dd[(node_num * ndof) + int(displacement[i, 1])] = displacement[i, 2]
        if displacement[i, 2] == 0.:
            np.append(model.positions, int((displacement[i, 0] * ndof) + displacement[i, 1]))   #Append command not working. Positions is still an empty array

    kstiff = getattr(model, 'kStif')
    np.delete(kstiff, model.positions, axis=0)
    np.delete(kstiff, model.positions, axis=1)

    setattr(model, 'uDisp', dd)
    setattr(model, 'kStif', kstiff)

    return
