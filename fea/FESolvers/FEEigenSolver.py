import numpy as np

def FEEigenSolver(a):
    values, vectors = np.linalg(a)

    freq = sqrt(values)
    