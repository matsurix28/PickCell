from plotly import graph_objects as go
from plotly.subplots import make_subplots


def show_fig(color3d, fvfm3d, scatter2d):
    fig = make_subplots(rows=1, cols=3,
                        specs=[
                            [{"type": "scatter3d"}, {"type": "scatter3d"},{'type': 'xy'}]
                        ])
    fig.add_trace((color3d), row=1, col=1)
    fig.add_trace((fvfm3d), row=1, col=2)
    fig.add_trace((scatter2d), row=1, col=3)
    fig.show()