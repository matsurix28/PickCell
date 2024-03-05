import colorsys
import time

import numpy as np
import pandas as pd
from plotly import express as px
from plotly import graph_objects as go


def main():
    g = Grr()
    g.main()

class Grr():
    def __init__(self):
        pass

    def main(self):
        df = pd.read_csv('2_res.csv', index_col=0)
        df = df.drop(columns='px')
        b = df['blue'].tolist()
        g = df['green'].tolist()
        r = df['red'].tolist()
        color = [[i,j,k] for (i,j,k) in zip(b,g,r)]
        df['px'] = color
        print('df size', len(df))
        #than = self._than_min_area(df)
        uniq = self._unique_px(df)
        hue_df = self.add_hue(uniq)
        self.draw_hist(hue_df)
        #print(than.head())

    def draw_hist(self, df):
        fig = px.histogram(df,'hue')
        #fig.show()
        hists, bins = np.histogram(df['hue'], range(0,55))
        fig = go.Figure(data=go.Scatter(x=bins, y=hists))
        fig.show()


    def rgb2hue(self, row):
        hsv = colorsys.rgb_to_hsv(row['red']/255, row['green']/255, row['blue']/255)
        hue = hsv[0] * 360
        return hue
    
    def add_hue(self, df: pd.DataFrame):
        result = df.assign(hue = lambda x: x.apply(self.rgb2hue, axis=1))
        return result
    
    def _than_min_area(self, df: pd.DataFrame):
        start = time.time()
        min_px = 10
        count_df = df[['blue', 'green', 'red']].value_counts()
        than = count_df[count_df > min_px].reset_index()
        b = than['blue'].tolist()
        g = than['green'].tolist()
        r = than['red'].tolist()
        color = [[i, j, k] for (i,j,k) in zip(b,g,r)]
        result = df[df['px'].isin(color)]
        end = time.time()
        print(end -start)
        return result
    
    def _unique_px(self, df: pd.DataFrame):
        uniq = df[['blue', 'green', 'red', 'fvfm']].drop_duplicates()
        return uniq
    
if __name__ == '__main__':
    main()