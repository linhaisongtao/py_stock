import matplotlib.pyplot as plt


class RoeChart(object):
    def show(self, sub_plot, roes):
        roes.reverse()

        x = []
        dates = []
        roe_list = []
        for index, roe in enumerate(roes):
            x.append(index)
            dates.append(roe.date[0:4])
            roe_list.append(roe.roe)
            pass

        last5 = roe_list[-5:]
        average5 = sum(last5) / len(last5)

        x.append(len(roes))
        roe_list.append(average5)
        dates.append("AVER")

        sub_plot.bar(x, roe_list)

        return {'x': x, 'dates': dates, 'average5': average5}
        pass

    pass
