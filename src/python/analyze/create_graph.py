import colorsys

import numpy as np
import pandas as pd
from plotly import graph_objects as go


class Graph():
    def __init__(self):
        pass

    def _unique_px(self, df: pd.DataFrame):
        uniq = df[['blue', 'green', 'red', 'fvfm']].drop_duplicates()
        return uniq
    
    def get_3dscatter_value(self, uniq_list):
        blue = [i[0,0] for i in uniq_list]
        green = [i[0,0] for i in uniq_list]
        red = [i[0,0] for i in uniq_list]
        fvfm_value = [i[1,0] for i in uniq_list]
        return blue, green, red, fvfm_value
    
    def get_2dscatter_value(self, uniq_list):
        color = [i[0] for i in uniq_list]
        hsv = [colorsys.rgb_to_hsv(i[2], i[1], i[0]) for i in color]
        hue = [i[0] for i in hsv]
        value = [i[1] for i in uniq_list]
        return hue, value, color
    
    def add_hue(self, df: pd.DataFrame):
        result = df.assign(hue = lambda x: x.apply(self.rgb2hue, axis=1))
        return result
    
    def draw_3dscatter(self, x, y, z, value=None, bar_title=None):
        marker = {'size': 1}
        if value is not None:
            marker.update(color=value)
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
    
    def input(self, px, fvfm):
        df = pd.DataFrame(px,
                          columns=['blue', 'green', 'red'])
        df['px'] = px
        df['fvfm'] = fvfm
        return df
    
    def draw(self, px, fvfm):
        df = self.input(px, fvfm)
        uniq_df = self._unique_px(df)
        hue_df = self.add_hue(uniq_df)
        b = hue_df['blue']
        g = hue_df['green']
        r = hue_df['red']
        h = hue_df['hue']
        fvfm = hue_df['fvfm']
        color = hue_df[['red', 'green', 'blue']].to_numpy().tolist()
        fig_l = self.draw_3dscatter(b,g,r, value=color)
        fig_h = self.draw_3dscatter(b,g,r, value=fvfm)
        c = self.rgb2color(color)
        fig_2d = self.draw_2dscatter(h, fvfm, marker_color=c)
        return fig_l, fig_h, fig_2d

    def _hue2rgb(self, hue):
        rgb = tuple(np.array(colorsys.hsv_to_rgb(hue/255, 1, 1)) * 255)
        result = f'rgb{rgb}'
        return result
    
    def rgb2color(self, rgb):
        color = [f'rgb({i[0]},{i[1]},{i[2]})' for i in rgb]
        return color
        
    def rgb2hue(self, row):
        hsv = colorsys.rgb_to_hsv(row['red']/255, row['green']/255, row['blue']/255)
        hue = hsv[0] * 360
        return hue