"""Contains the respective visualization tasks."""
import mpld3
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, *args, **kwargs):
        pass

    def pie_plot(self, **kwargs):

        fig1, ax1 = plt.subplots()
        ax1.pie(kwargs['sizes'],
                explode=kwargs['explode'],
                labels=kwargs['labels'],
                autopct='%1.1f%%',
                shadow=True,
                startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        return mpld3.fig_to_html(fig1)
