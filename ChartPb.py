import matplotlib.pyplot as plt


class PbChart(object):
    def show(self, sub_plot, pb_list):

        x = []
        dates = []
        pbs = []
        for index, pb in enumerate(pb_list):
            x.append(index)
            dates.append(pb.date)
            pbs.append(pb.pb)
            pass
        sub_plot.plot(x, pbs)

        sorted_pb = sorted(pbs)
        count = len(sorted_pb)

        pb20 = sorted_pb[int(count * 0.2)]
        pb50 = sorted_pb[int(count * 0.5)]
        pb80 = sorted_pb[int(count * 0.8)]
        pb_now = pbs[len(pbs) - 1]
        sub_plot.axhline(pb20, color='g', linestyle='--', linewidth=1)
        sub_plot.axhline(pb50, color='y', linestyle='--', linewidth=1)
        sub_plot.axhline(pb80, color='r', linestyle='--', linewidth=1)

        count = len(dates) / 5
        for index, label in enumerate(dates):
            if index != 0 and (index + 1) % count != 0:
                dates[index] = ''
                pass
            pass
        plt.title("now=%.2f pb20=%.2f pb50=%.2f pb80=%.2f" % (pb_now, pb20, pb50, pb80))
        return {'x': x, 'dates': dates, 'pb20': pb20, 'pb50': pb50, "pb80": pb80, "pb_now": pb_now}
        pass

    pass
