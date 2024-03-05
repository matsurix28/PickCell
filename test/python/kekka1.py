import numpy as np
from plotly import graph_objects as go
import colorsys

class Graph():
    def __init__(self):
        pass

    def _unique_px(self, px, value):
        val_list = [[i,0,0] for i in value]
        gti_list = np.stack([px, val_list], 1)
        uniq_list = np.unique(gti_list, axis=0)
        return uniq_list

    def _than_min_area(self, px_list, value_list):
        px = []
        value = []
        min_count = len(px_list) / 1000
        for p, v in zip(px_list, value_list):
            if px_list.count(p[0]) > min_count:
                px.append(p)
                value.append(v)
        return px, value
    
    def get_3dscatter_value(self, px_list, value_list):
        px, value = self._than_min_area(px_list, value_list)
        uniq_px_list = self._unique_px(px, value)
        blue = [i[0,0] for i in uniq_px_list]
        green = [i[0,0] for i in uniq_px_list]
        red = [i[0,0] for i in uniq_px_list]
        fvfm_value = [i[1,0] for i in uniq_px_list]
        return blue, green, red, fvfm_value
    
    def get_2dscatter_value(self, px_list, value_list):
        px, value = self._than_min_area(px_list, value_list)
        uniq_px_list = self._unique_px(px, value)
        color = [i[0] for i in uniq_px_list]
        hsv = [colorsys.rgb_to_hsv(i[2], i[1], i[0]) for i in color]
        hue = [i[0] for i in hsv]
        value = [i[1] for i in uniq_px_list]
        return hue, value, color
    
    def draw_3dscatter(self, x, y, z, value=None, bar_title=None):
        marker = {'size': 1}
        if value is not None:
            marker{'color': value}
            if bar_title is not None:
                marker['colorbar'] = {'title': bar_title}
        fig = go.Figure(
            data=[go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=marker
            )]
        )
        return fig
    
    def draw_2dscatter(self, x, y, marker_color):
        marker = {
            'size': 5,
            'color': marker_color,
        }
        fig = go.Figure(
            data=[go.Scatter(
                x=x,
                y=y,
                mode='markers',
                marker=marker
            )]
        )
        return fig

    def _hue2rgb(self, hue):
        rgb = tuple(np.array(colorsys.hsv_to_rgb(hue/255, 1, 1)) * 255)
        result = f'rgb{rgb}'
        return result