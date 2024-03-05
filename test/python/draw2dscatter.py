import colorsys

import numpy as np
from plotly import graph_objects as go

hue = [20,30,40,50,10]
val = [79,78,77,70,80]

def hue2rgb(hue):
    rgb = tuple(np.array(colorsys.hsv_to_rgb(hue/255,1,1)) * 255)
    result = f'rgb{rgb}'
    return result

#marker_color = [list(np.array(colorsys.hsv_to_rgb(i/255,1,1)) * 255) for i in hue]
marker_color = [hue2rgb(i) for i in hue]
print(marker_color)
marker = {'size': 10}
marker.update(color=marker_color)
#marker['colorbar'] = {'title': 'Fv/Fm'}

figure = go.Figure(
    data=[go.Scatter(
        x=hue,
        y=val,
        mode='markers',
        marker=marker,
        #marker_color=marker_color
    )]
)

figure.show()