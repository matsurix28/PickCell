from plotly import graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2,
                    specs=[
                        [{"type": "scene"}, {"type": "scene"}],[{'type': 'xy'}, {'type': 'xy'}]
                    ])

px1 = [[255,20,20], [230,10,10], [200, 50,50]]
px2 = [[20,20,255], [10,10,230], [50,50,200]]

r1 = [i[0] for i in px1]
g1 = [i[1] for i in px1]
b1 = [i[2] for i in px1]

r2 = [i[0] for i in px2]
g2 = [i[1] for i in px2]
b2 = [i[2] for i in px2]

marker1 = {'size': 1}
marker1.update(color=px1)

marker2 = {'size': 1}
marker2.update(color=px2)

fig.add_trace(go.Scatter3d(
    x=r1, y=g1, z=b1,mode='markers',
    marker=marker1,
), row=1, col=1)

fig.add_trace(go.Scatter3d(
    x=r2, y=g2, z=b2,mode='markers',
    marker=marker2
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=r1, y=g1,
    mode='markers'
), row=2, col=1)

fig.show()