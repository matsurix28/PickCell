import pandas as pd

px = [[23,34,45], [11,56,67], [11,90,100], [23,23,22], [23,34,45], [11,90,100]]
fvfm = [780, 790, 780, 500, 790, 700]
val = [300,400,300,500,900]

'''
df = pd.DataFrame(px,
                  columns=['Blue', 'Green', 'Red'])
df['FvFm'] = fvfm
#print(df)

#a = df[['Blue', 'Green', 'Red']].astype(str).apply(lambda x: [i for i in x], axis=1).str.join(',').value_counts()
a = df[['Blue', 'Green', 'Red']].value_counts(sort=True).reset_index()
res = a[a['count'] > 1]

ddf = pd.DataFrame({
    'px': px,
    'fvfm': fvfm
})
a = ddf['px'].value_counts(sort=True)
res = a[a > 1].reset_index()
than_px = res['px'].tolist()
than = ddf[ddf['px'].isin(than_px)]
#print(than)

b = pd.DataFrame(px,
                 columns=['Blue', 'Green', 'Red'])
b['px'] = px
b['fvfm'] = fvfm
count_df = b['px'].value_counts(sort=True)
count = count_df[count_df > 1].reset_index()['px'].tolist()
than_px = b[b['px'].isin(count)]
#print(b)

uniq = than_px[['Blue', 'Green', 'Red', 'fvfm']].drop_duplicates()
#print(uniq)
'''
import colorsys


def rgb2hue(row):
    hsv = colorsys.rgb_to_hsv(row['red']/255, row['green']/255, row['blue']/255)
    hue = hsv[0]
    return hue

#c=b.assign(hue = lambda x: x.apply(rgb2hue, axis=1))
#print(c)


df = pd.DataFrame(px,
                  columns=['blue', 'green', 'red'])

df['fvfm'] = fvfm
df['px'] = px
c=df.assign(hue = lambda x: x.apply(rgb2hue, axis=1))
cont_df = c[['blue', 'green', 'red']].value_counts()
than = cont_df[cont_df > 1].reset_index()
b = than['blue'].tolist()
g = than['green'].tolist()
r = than['red'].tolist()
col0r = [[i,j,k] for (i,j,k) in zip(b,g,r)]
res = df[df['px'].isin(col0r)]
print(res)