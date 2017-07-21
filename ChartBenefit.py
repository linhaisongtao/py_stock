import matplotlib.pyplot as plt
import numpy as np
import math


class BenefitChart(object):
    def show(self, sub_plot, roe_data, pb_data):
        x = np.arange(0, 11)
        pb20 = pb_data['pb20']
        pb_now = pb_data['pb_now']
        pures = []
        sell20 = []
        for i in x:
            pure = math.pow(1 + roe_data['average5'] / 100, i)
            pures.append(pure - 1)
            sell20.append((pure - pb20) / pb_now)
            pass

        sub_plot.plot(x, pures, color='y')
        sub_plot.plot(x, sell20, color='b')
        sub_plot.axhline(0, color='darkgray', linestyle=':')
        sub_plot.axhline(1, color='darkgray', linestyle=':')
        sub_plot.axhline(3, color='darkgray', linestyle=':')
        sub_plot.axvline(5, color='darkgray', linestyle=':')
        sub_plot.axvline(10, color='darkgray', linestyle=':')
        sub_plot.legend(['pure', 'sell20'])
        plt.title("pure=%.2f sell20=%.2f" % (pures[len(pures) - 1], sell20[len(sell20) - 1]))
        pass

    pass
