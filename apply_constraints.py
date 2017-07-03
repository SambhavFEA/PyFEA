
import numpy as np

def apply_constraints (part):

    positions= np.zeros([])

    ndof  = getattr(part,'ndof')
    nnpe = getattr(part,'nnpe')

    forces = getattr(part,'forces')
    forces_size = np.shape(forces)
    ff = getattr(part,'fForce')

    for i in forces_size(0):
        node_num = forces[i,0]
        ff[node_num*ndof] = forces[i,1]
        ff[(node_num * ndof)+1] = forces[i, 2]

    setattr(part,'fForce',ff)

    displacement = getattr(part,'constraints')
    disp_size = np.shape(displacement)
    dd = getattr(part,'uDisp')

    for i in disp_size(0):
        node_num = displacement[i,0]
        dd[(node_num*ndof) + displacement[i,1]] = displacement[i,2]
        if displacement[i,2]==0 :
            np.append(positions,(displacement[i,0]*ndof) + displacement[i,1],axis=0)

    kstiff = getattr(part,'kStiff')
    np.delete(kstiff,positions,axis=0)
    np.delete(kstiff, positions, axis=1)

    setattr(part, 'uDisp', dd)
    setattr(part, 'kStiff', kstiff)

    return
