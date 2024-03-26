from plotly import graph_objects as go
from plotly.subplots import make_subplots


def test():
    from create_graph import Graph
    g = Graph()
    px = [[200,34,45], [45,56,67], [100,120,150]]
    fvfm = [0.6, 0.7, 0.8]
    fig1, fig2, fig3 = g.draw(px, fvfm)
    fig = multi_graph(fig1, fig2, fig3)
    fig.show()

def multi_graph(color3d, fvfm3d, scatter2d):

    fig = make_subplots(rows=1, cols=3,
                        specs=[
                            [{'type': 'xy'},{"type": "scatter3d"}, {"type": "scatter3d"}]
                        ],
                        subplot_titles=['Hue and Fv/Fm', 'Color scatter', 'Fv/Fm scatter'])
    
    fig.update_layout(showlegend=False)
    fig.add_trace(scatter2d['data'][0], row=1, col=1)
    fig.add_trace(color3d['data'][0], row=1, col=2)
    fig.add_trace(fvfm3d['data'][0], row=1, col=3)
    fig['layout']['xaxis']['title'] = 'Hue'
    fig['layout']['yaxis']['title'] = 'Fv/Fm'
    fig['layout']['scene']['xaxis']['title'] = 'Blue'
    fig['layout']['scene']['yaxis']['title'] = 'Green'
    fig['layout']['scene']['zaxis']['title'] = 'Red'
    fig['layout']['scene2']['xaxis']['title'] = 'Blue'
    fig['layout']['scene2']['yaxis']['title'] = 'Green'
    fig['layout']['scene2']['zaxis']['title'] = 'Red'
    fig['layout']['scene']['xaxis']['range'] = [0, 255]
    fig['layout']['scene']['yaxis']['range'] = [0, 255]
    fig['layout']['scene']['zaxis']['range'] = [0, 255]
    fig['layout']['scene2']['xaxis']['range'] = [0, 255]
    fig['layout']['scene2']['yaxis']['range'] = [0, 255]
    fig['layout']['scene2']['zaxis']['range'] = [0, 255]
    print(fig)
    return fig

if __name__ == '__main__':
    test()
