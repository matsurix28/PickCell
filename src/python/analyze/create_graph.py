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
    
    '''
    def _unique_px(self, px, value):
        val_list = [[i,0,0] for i in value]
        gti_list = np.stack([px, val_list], 1)
        uniq_list = np.unique(gti_list, axis=0)
        return uniq_list
    '''
        
    '''
    def _than_min_area(self, px_list, value_list):
        px = []
        value = []
        min_count = len(px_list) / 1000
        print('min count', min_count)
        print('px1', px_list[0])
        print('count', px_list.count(px_list[0]))
        c = 0
        for p, v in zip(px_list, value_list):
            print(c)
            if int(px_list.count(p)) > min_count:
                px.append(p)
                value.append(v)
            c += 1
        return px, value
    '''

    def _than_min_area(self, df: pd.DataFrame):
        min_px = 10
        count_df = df[['blue', 'green', 'red']].value_counts()
        print('countdf')
        than = count_df[count_df > min_px].reset_index()
        print('than tahn')
        b = than['blue'].tolist()
        g = than['green'].tolist()
        r = than['red'].tolist()
        print('bgr')
        color = [[i,j,k] for (i,j,k) in zip(b,g,r)]
        print('color')
        result = df[df['px'].isin(color)]
        return result
    
    def get_3dscatter_value(self, uniq_list):
        #px, value = self._than_min_area(px_list, value_list)
        #uniq_px_list = self._unique_px(px, value)
        blue = [i[0,0] for i in uniq_list]
        green = [i[0,0] for i in uniq_list]
        red = [i[0,0] for i in uniq_list]
        fvfm_value = [i[1,0] for i in uniq_list]
        return blue, green, red, fvfm_value
    
    def get_2dscatter_value(self, uniq_list):
        #px, value = self._than_min_area(px_list, value_list)
        #uniq_px_list = self._unique_px(px, value)
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
        '''
        fig = go.Figure(
            data=[go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=marker
            )]
        )
        '''
        data=go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=marker
            )
        return data
    
    def draw_2dscatter(self, x, y, marker_color):
        marker = {
            'size': 5,
            'color': marker_color,
        }
        '''
        fig = go.Figure(
            data=[go.Scatter(
                x=x,
                y=y,
                mode='markers',
                marker=marker
            )]
        )
        '''
        data=[go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=marker
            )]
        return data
    
    def input(self, px, fvfm):
        df = pd.DataFrame(px,
                          columns=['blue', 'green', 'red'])
        df['px'] = px
        df['fvfm'] = fvfm
        df.to_csv('2_res.csv')
        return df
    
    def draw(self, px, fvfm):
        df = self.input(px, fvfm)
        print('than')
        #than_df = self._than_min_area(df)
        print('uniq')
        uniq_df = self._unique_px(df)
        print('add hue')
        hue_df = self.add_hue(uniq_df)
        #print(uniq)
        #print('get 3d val')
        #blue, green, red, fvfm = self.get_3dscatter_value(uniq)
        #print('get 2d val')
        #hue, _, color = self.get_2dscatter_value(uniq)
        print('draw 3d leaf')
        b = hue_df['blue']
        g = hue_df['green']
        r = hue_df['red']
        h = hue_df['hue']
        fvfm = hue_df['fvfm']
        color = hue_df[['red', 'green', 'blue']].to_numpy().tolist()
        print('draw 3d')
        fig_l = self.draw_3dscatter(b,g,r, value=color)
        print('drw 3d fvfm')
        fig_h = self.draw_3dscatter(b,g,r, value=fvfm)
        print('drw 2d')
        c = self.rgb2color(color)
        fig_2d = self.draw_2dscatter(h, fvfm, marker_color=c)
        print('finish')
        return fig_l, fig_h, fig_2d
        '''
        red = [i[2] for i in px]
        green = [i[1] for i in px]
        blue = [i[0] for i in px]

        hue = red
        color = [[i[2], i[1], i[0]] for i in px]
        c = [f'rgb({i[0]}, {i[1]}, {i[2]})' for i in color]

        fig_leaf = self.draw_3dscatter(red, green, blue, value=color)
        print('draw 3d fvfm')
        fig_fvfm = self.draw_3dscatter(red, green, blue, value=fvfm, bar_title='Fv/Fm')
        print('draw 2d')
        fig_hue = self.draw_2dscatter(hue, fvfm, marker_color=c)
        #fig_leaf.show()
        #fig_fvfm.show()
        return fig_leaf, fig_fvfm, fig_hue
        '''

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