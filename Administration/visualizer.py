"""Contains the respective visualization tasks."""
import plotly.plotly as py
from plotly.graph_objs import *


class Visualizer:
    def __init__(self, *args, **kwargs):
        pass

    py.sign_in('kasramvd', 'api_key')

    data = Data([trace1, trace2, trace3, trace4])
    layout = {"font": {"size": 16},
              "legend": {"font": {"size": 16}},
              "orientation": 270,
              "radialaxis": {"ticksuffix": "%"},
              "title": "Wind Speed Distribution in Laurel, NE"}

    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)
