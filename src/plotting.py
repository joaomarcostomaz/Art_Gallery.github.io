import plotly.graph_objects as go
import numpy as np

def plot_polygon(polygon):
    x, y = zip(*polygon)
    fig = go.Figure(data=[go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                                     mode='lines+markers', 
                                     fill='toself')])
    return fig    

def animate_triangulation(polygon, triangles):
    frames = []
    x, y = zip(*polygon)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             name='Polygon'))
    
    for step in range(len(triangles)):
        frame_data = [go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                                 mode='lines+markers', 
                                 name='Polygon')]
        
        for i in range(step + 1):
            x_tri, y_tri = zip(*triangles[i])
            frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                         mode='lines', fill='toself',
                                         name=f'Triangle {i + 1}'))
        frames.append(go.Frame(data=frame_data, name=f'Step {step + 1}'))
        fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             name='Polygon'))
        
    frames.insert(0, go.Frame(data=[go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                                               mode='lines+markers', 
                                                name='Polygon')], 
                                                name='Start'))

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
        title="Polygon Final Triangulation",
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        showlegend=True
    )

    return fig

def plot_colored_polygon(polygon, coloring):
    x, y = zip(*polygon)
    colors = [coloring[tuple(vertex)] for vertex in polygon]
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

def is_convex(prev, curr, next):
    return (curr[0] - prev[0]) * (next[1] - curr[1]) - (curr[1] - prev[1]) * (next[0] - curr[0]) > 0

def is_point_in_triangle(p, a, b, c):
    d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    w1 = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / d
    w2 = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / d
    w3 = 1 - w1 - w2
    return 0 <= w1 <= 1 and 0 <= w2 <= 1 and 0 <= w3 <= 1

def is_ear(polygon, i):
    n = len(polygon)
    prev = polygon[(i-1)%n]
    curr = polygon[i]
    next = polygon[(i+1)%n]
    
    if not is_convex(prev, curr, next):
        return False
    
    for j in range(n):
        if j in [(i-1)%n, i, (i+1)%n]:
            continue
        if is_point_in_triangle(polygon[j], prev, curr, next):
            return False
    return True

def animate_triangulation_2(polygon):
    x, y = zip(*polygon)
    n = len(polygon)
    if n < 3:
        return []
    remaining_vertices = polygon[:]
    triangles = []
    frames = []
    while len(remaining_vertices) > 3:
        for i in range(len(remaining_vertices)):
            prev = remaining_vertices[i-1]
            curr = remaining_vertices[i]
            next = remaining_vertices[(i+1)%len(remaining_vertices)]
            
            frames.append(go.Frame(data=[
                go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                               mode='lines', name='Polygon'),
                go.Scatter(x=[prev[0],curr[0],next[0]], y=[prev[1],curr[1],next[1]],
                        mode='lines',
                        marker=dict(size=12, color='red'),
                        name='Current possible triangle')
            ]))
                
            if is_ear(remaining_vertices, i):
                triangles.append([prev, curr, next])
                del remaining_vertices[i]
                
                frames.append(go.Frame(data=[
                    go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                               mode='lines', name='Polygon'),
                    go.Scatter(x=[point[0] for triangle in triangles for point in triangle] + [triangles[-1][0][0]],
                               y=[point[1] for triangle in triangles for point in triangle] + [triangles[-1][0][1]],
                               mode='lines', name='Triangles')
                ]))
                
                break
    triangles.append(remaining_vertices)
    frames.append(go.Frame(data=[
        go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                   mode='lines', name='Polygon'),
        go.Scatter(x=[point[0] for triangle in triangles for point in triangle] + [triangles[-1][0][0]],
                   y=[point[1] for triangle in triangles for point in triangle] + [triangles[-1][0][1]],
                   mode='lines', name='Triangles')
    ]))
    
    return frames

def plot_test(polygon):
    x, y = zip(*polygon)
    frames = animate_triangulation_2(polygon)
    fig = go.Figure(
        data=[
            go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                    mode='lines', name='Polygon')
        ],
        frames=frames,
        layout=go.Layout(
            title="Polygon Triangulation",
            updatemenus=[dict(type='buttons', showactive=False,
                            buttons=[
                                dict(label='Play',
                                    method='animate',
                                    args=[None, dict(frame=dict(duration=500, redraw=True), 
                                                        fromcurrent=True)]),
                                dict(label='Pause',
                                    method='animate',
                                    args=[[None], dict(frame=dict(duration=0, redraw=False), 
                                                        mode='immediate')])
                            ])],
            sliders=[{
                'steps': [{'args': [[f.name], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate'}],
                        'label': f'Frame {k}',
                        'method': 'animate'} for k, f in enumerate(frames)],
                'transition': {'duration': 300},
                'x': 0.1,
                'len': 0.9
            }]
        )
    )
    return fig