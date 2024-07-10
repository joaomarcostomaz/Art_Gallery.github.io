import plotly.graph_objects as go
import numpy as np

def is_convex(prev, curr, next):
    return (curr[0] - prev[0]) * (next[1] - curr[1]) - (curr[1] - prev[1]) * (next[0] - curr[0]) > 0

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

def is_point_in_triangle(p, a, b, c):
    # Barycentric coordinates
    d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    w1 = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / d
    w2 = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / d
    w3 = 1 - w1 - w2
    return 0 <= w1 <= 1 and 0 <= w2 <= 1 and 0 <= w3 <= 1

def ear_clipping_triangulation(polygon):
    n = len(polygon)
    if n < 3:
        return []

    remaining_vertices = polygon[:]
    triangles = []
    while len(remaining_vertices) > 3:
        for i in range(len(remaining_vertices)):
            if is_ear(remaining_vertices, i):
                prev = remaining_vertices[i-1]
                curr = remaining_vertices[i]
                next = remaining_vertices[(i+1)%len(remaining_vertices)]
                triangles.append([prev, curr, next])
                del remaining_vertices[i]
                break
    triangles.append(remaining_vertices)
    return triangles
    
def plot_triangles(polygon, triangles):
    frames = []
    print("entrei")
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


def animate_triangulation(polygon):
    n = len(polygon)
    if n < 3:
        return []
    remaining_vertices = polygon[:]
    triangles = []
    frames = []
    contador = 0
    while len(remaining_vertices) > 3:
        for i in range(len(remaining_vertices)):
            prev = remaining_vertices[i-1]
            curr = remaining_vertices[i]
            next = remaining_vertices[(i+1)%len(remaining_vertices)]
            frame_data = [
                go.Scatter(x=tuple(sublist[0] for sublist in remaining_vertices) + (remaining_vertices[0][0],) , 
                            y=tuple(sublist[1] for sublist in remaining_vertices) + (remaining_vertices[0][1],), 
                                mode='lines+markers', name='Polygon'),
                
                go.Scatter(x=[prev[0],curr[0],next[0],prev[0]], 
                    y=[prev[1],curr[1],next[1],prev[1]],
                    mode='lines+markers',
                    marker=dict(size=12, color='red'),
                    fill='toself',
                    name='Current possible triangle')
            ]
            
            frames.append(go.Frame(data=frame_data))
            
            if is_ear(remaining_vertices, i):
                triangles.append([prev, curr, next])
                del remaining_vertices[i]
                break
    triangles.append(remaining_vertices)
    
    frame_data =[
        go.Scatter(x=tuple(sublist[0] for sublist in remaining_vertices) + (remaining_vertices[0][0],) , y=tuple(sublist[1] for sublist in remaining_vertices) + (remaining_vertices[0][1],), 
                       mode='lines+markers', name='Polygon'),
        go.Scatter(x=tuple(sublist[0] for sublist in remaining_vertices) + (remaining_vertices[0][0],) , y=tuple(sublist[1] for sublist in remaining_vertices) + (remaining_vertices[0][1],),
            mode='lines+markers',
            marker=dict(size=12, color='red'),
            fill='toself',
            name='Current possible triangle')
    ]
    
    frames.append(go.Frame(data=frame_data))

    
    frame_data =[
        go.Scatter(x=[] , y=[], 
                       mode='lines+markers', name='Polygon'),
        go.Scatter(x=[] , y=[], 
                       mode='lines+markers', name='Polygon'),
    ]
    
    frames.append(go.Frame(data=frame_data))

    return frames

def plot_triangulation(polygon):
    x, y = zip(*polygon)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             name='Polygon'))
    
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],),
                            mode='markers',
                            marker=dict(color='red'),
                            name='Vertices'))
    
    frames = animate_triangulation(polygon)
    fig.frames = frames
    fig.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=True,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=600, redraw=True), 
                                 fromcurrent=True, mode='immediate')]
            )]
        )],
        xaxis=dict(range=[min(x) - 1, max(x) + 1]),
        yaxis=dict(range=[min(y) - 1, max(y) + 1])
    ),
    
    fig.update_layout(
        title="Triangle",
        showlegend=True
    )

    return fig

