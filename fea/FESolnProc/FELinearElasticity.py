from FESolnProc import FESolnProc


class FELinearElasticity(FESolnProc):
    model_list = ['FELinearModel']
    material_list = ['FEPlaneStress2D', 'FEPlaneStrain']

    def __init__(self):
        pass
