from plotly import graph_objects as go
from plotly.subplots import make_subplots


def show_sctter3d(fig1, fig2, fig3):
    fig = make_subplots(
        rows=1, cols=3,
        specs=[
            [{'type': 'scene'}, {'type': 'scene'}, {'type': 'xy'}]
        ]
    )
    fig.add_traces(fig1.data[0], rows=1, cols=1)
    fig.add_traces(fig2.data[0], rows=1, cols=2)
    fig.add_traces(fig3.data[0], rows=1, cols=3)
    fig.show()