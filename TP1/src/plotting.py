import plotly.graph_objects as go

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
        title="Polygon Triangulation",
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