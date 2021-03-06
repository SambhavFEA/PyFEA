import numpy as np


class FEIsoParaQuadElement(object):

    ndof = 8
    num_of_nodes = 4

    def __init__(self, *args):
        """
        :param args: args must be a list of four tuples. e.g. [(1,2), (3,4), (5,6), (7,8)]
        """
        leng = len(args[0])
        if leng == 4:
            self.pt = []
            flag = 0

            for i in range(leng):
                if isinstance(args[0][i], tuple):
                    self.pt.append(args[0][i])
                else:
                    flag = 1
            if flag == 1:
                raise ValueError('Points for FEIsoParaQuadElement must be tuple')
        else:
            raise ValueError('Not enough points for FEIsoParaQuadElement. Need 4 points.')

    @staticmethod
    def get_n1(s, t):
        return 0.25 * (1. - s) * (1. - t)

    @staticmethod
    def get_n2(s, t):
        return 0.25 * (1. + s) * (1. - t)

    @staticmethod
    def get_n3(s, t):
        return 0.25 * (1. + s) * (1. + t)

    @staticmethod
    def get_n4(s, t):
        return 0.25 * (1. - s) * (1. + t)

    def get_n(self, s, t):
        return [[self.get_n1(s, t), 0., self.get_n2(s, t), 0., self.get_n3(s, t), 0., self.get_n4(s, t), 0.],
                [0., self.get_n1(s, t), 0., self.get_n2(s, t), 0., self.get_n3(s, t), 0., self.get_n4(s, t)]]

    @staticmethod
    def get_dn1(s, t):
        return [0.25 * (-1. + t), 0.25 * (-1. + s)]

    @staticmethod
    def get_dn2(s, t):
        return [0.25 * (1. - t), 0.25 * (-1. - s)]

    @staticmethod
    def get_dn3(s, t):
        return [0.25 * (1. + t), 0.25 * (1. + s)]

    @staticmethod
    def get_dn4(s, t):
        return [0.25 * (-1. - t), 0.25 * (1. - s)]

    def get_all_dn(self, s, t):
        transdn = np.array([self.get_dn1(s, t), self.get_dn2(s, t), self.get_dn3(s, t), self.get_dn4(s, t)])
        return transdn.transpose()

    def get_all_x(self):
        return np.array([self.pt[0][0], self.pt[1][0], self.pt[2][0], self.pt[3][0]])

    def get_all_y(self):
        return np.array([self.pt[0][1], self.pt[1][1], self.pt[2][1], self.pt[3][1]])

    def get_all_pts(self):
        return self.pt

    def get_area(self):
        a = np.linalg.norm(np.array(self.pt[0]) - np.array(self.pt[1])) ** 2
        b = np.linalg.norm(np.array(self.pt[1]) - np.array(self.pt[2])) ** 2
        c = np.linalg.norm(np.array(self.pt[2]) - np.array(self.pt[3])) ** 2
        d = np.linalg.norm(np.array(self.pt[3]) - np.array(self.pt[0])) ** 2
        p = np.linalg.norm(np.array(self.pt[0]) - np.array(self.pt[2])) ** 2
        q = np.linalg.norm(np.array(self.pt[1]) - np.array(self.pt[3])) ** 2

        return 0.25 * ((4. * p * q) - (b + d - a - c)) ** 0.5

    def get_jacobian(self, s, t):
        dn = np.array(self.get_all_dn(s, t))
        xy = np.array([self.get_all_x(), self.get_all_y()]).transpose()

        j = np.matmul(dn, xy)

        return j

    def get_b_matrix(self, s, t):
        tempa = np.zeros([4,4])
        tempa[0:2, 0:2] = np.linalg.inv(self.get_jacobian(s, t))
        tempa[2:4, 2:4] = tempa[0:2, 0:2]
        a_matrix = np.matmul(np.array([[1., 0., 0., 0.], [0., 0., 0., 1.], [0., 1., 1., 0.]]), tempa)

        g_matrix = np.zeros([4, 8])
        g_matrix[0:2, 0] = g_matrix[2:4, 1] = self.get_dn1(s, t)
        g_matrix[0:2, 2] = g_matrix[2:4, 3] = self.get_dn2(s, t)
        g_matrix[0:2, 4] = g_matrix[2:4, 5] = self.get_dn3(s, t)
        g_matrix[0:2, 6] = g_matrix[2:4, 7] = self.get_dn4(s, t)

        return np.matmul(a_matrix, g_matrix)
