from src.vertex_coloring import color_vertices
import plotly.graph_objects as go


def minimum_camera_positions(triangles):
    vertexColors = color_vertices(triangles)
    
    colorPartitions = {'purple': [], 'green': [], 'blue': []}
    for vertex, color in vertexColors.items():
        colorPartitions[color].append(vertex)
    
    smallestPartition = min(colorPartitions.values(), key=len)
    cameraPositions = list(set(smallestPartition))
    
    return cameraPositions

def animate_cameras(polygon, cameras):
    x, y = zip(*polygon)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers',
                            line=dict(width=1, color='black'),
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