class GaussLegendreQuadrature(object):

    w = [[2],
         [1, 1],
         [5/9, 8/9, 5/9]]

    r = [[0],
         [0.57735, -0.57735],
         [0.774597, 0, -0.774597]]

    @staticmethod
    def integration(func, order):
        w = GaussLegendreQuadrature.w
        r = GaussLegendreQuadrature.r
        value = 0.;

        for i in range(order):
            value = value + (w[order - 1][i] * func(r[order - 1][i]))

        return value

    @staticmethod
    def dblintegration(func, order):
        """
        :param func:
        :param order: order of the function, must be integer and greater than 0.
        :return:
        """

        w = GaussLegendreQuadrature.w
        r = GaussLegendreQuadrature.r
        value = 0.;

        for j in range(order):
            for i in range(order):
                value = value + (w[order - 1][i] * w[order - 1][j] * func(r[order - 1][i], r[order - 1][j]))

        return value
