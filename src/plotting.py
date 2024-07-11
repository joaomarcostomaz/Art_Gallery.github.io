import plotly.graph_objects as go
import numpy as np

def plot_polygon(polygon):
    x, y = zip(*polygon)
    fig = go.Figure(data=[go.Scatter(x=x+ (x[0],), y=y + (y[0],), 
                                     mode='lines+markers', 
                                     fill='toself')])
    
    fig.update_layout(
        title="Polygon",
        showlegend=True
    )
    return fig    

