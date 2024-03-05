import collections

px = [[23,33,45],[12,23,21], [55,43,22], [12,44,55], [12,23,45], [12,23,21],[12,23,12]]
c = collections.Counter(px)
val = [3,5,6,4,1, 2,0]
res = []
for i in range(len(px)):
    res.append([px[i], val[i]])
a = sorted(res)
a
c.most_common()
px.count([12,23,21])
ato = []
for r in res:
    if px.count(r[0]) > 1:
        ato.append(r)