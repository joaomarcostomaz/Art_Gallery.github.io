import plotly.graph_objects as go
import numpy as np

def plot_polygon(polygon):
    x, y = zip(*polygon)
    fig = go.Figure(data=[go.Scatter(x=x+ (x[0],), y=y + (y[0],), 
                                     mode='lines+markers', 
                                     fill='toself')])
    return fig    


def plot_colored_polygon(polygon, coloring):
    x, y = zip(*polygon)
    colors = [coloring[tuple(vertex)] for vertex in polygon] + [coloring[tuple(polygon[0])]]
    print(colors)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             marker=dict(color=colors, size=10),
                             name='Polygon'))
    return fig

def animate_cameras(polygon, cameras):
    x, y = zip(*polygon)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             name='Polygon'))

    camera_x = [camera[0] for camera in cameras]
    camera_y = [camera[1] for camera in cameras]
    fig.add_trace(go.Scatter(x=camera_x, y=camera_y,
                             mode='markers',
                             marker=dict(size=12, color='red'),
                             name='Cameras'))
    frames = []
    for step in range(1, len(cameras) + 1):
        frames.append(go.Frame(data=[
            go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                       mode='lines+markers', 
                       name='Polygon'),
            go.Scatter(x=camera_x[:step], y=camera_y[:step], 
                       mode='markers', 
                       marker=dict(size=12, color='red'), 
                       name='Cameras')
        ], name=f'Step {step}'))

    fig.frames = frames
    fig.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=True,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=500, redraw=True), 
                                 fromcurrent=True, mode='immediate')]
            )]
        )],
        xaxis=dict(range=[min(x) - 1, max(x) + 1]),
        yaxis=dict(range=[min(y) - 1, max(y) + 1])
    )

    fig.update_layout(
        title="Polygon with Cameras",
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        showlegend=True
    )

    return fig