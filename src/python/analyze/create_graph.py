import colorsys

import numpy as np
import pandas as pd
from plotly import graph_objects as go

def test():
    g = Graph()
    px = [[200,34,45], [45,56,67], [100,120,150]]
    fvfm = [0.6, 0.7, 0.8]
    fig1, fig2, fig3 = g.draw(px, fvfm)
    fig3.show()

class Graph():
    def __init__(self):
        self.set_val()

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
    
    def draw_3dscatter(self, x, y, z, value=None, bar_title=None, fig_title=None):
        marker = {'size': self.size_3d}
        if value is not None:
            marker.update(color=value)
            if bar_title is not None:
                marker['colorbar'] = {'title': bar_title}
                marker['colorscale'] = 'Jet'
        scene = dict(
            xaxis = dict(
                range=[0,255],
                title='Blue'
            ),
            yaxis = dict(
                range = [0, 255],
                title = 'Green'
            ),
            zaxis = dict(
                range = [0, 255],
                title = 'Red'
            )
        )
        fig = go.Figure(
            data=[go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=marker,
                name='Color'
            )]
        )
        fig.update_layout(
            scene=scene
        )
        if fig_title is not None:
            fig.update_layout(title = fig_title)
        return fig
    
    def draw_2dscatter(self, x, y, marker_color, fig_title=None):
        marker = {
            'size': self.size_2d,
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
        fig.update_layout(
            xaxis = dict(title = 'Hue'),
            yaxis = dict(title = 'Fv/Fm')
        )
        if fig_title is not None:
            fig.update_layout(title = fig_title)
        return fig
    
    def set_val(self, size_2d=5, size_3d=1):
        self.size_2d = size_2d
        self.size_3d = size_3d
    
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
        fig_l = self.draw_3dscatter(b,g,r, value=color, fig_title='Color Scatter')
        fig_h = self.draw_3dscatter(b,g,r, value=fvfm, bar_title='Fv/Fm', fig_title='Fv/Fm Scatter')
        c = self.rgb2color(color)
        fig_2d = self.draw_2dscatter(h, fvfm, marker_color=c, fig_title='Hue and Fv/Fm')
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

if __name__ == '__main__':
    test()
