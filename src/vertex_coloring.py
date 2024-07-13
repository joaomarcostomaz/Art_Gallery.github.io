import networkx as nx
import plotly.graph_objects as go

def create_dual_graph(triangles):
    """
    Creates a dual graph from a list of triangles.

    Parameters:
        triangles: A list of triangles. A triangle is a list of vertices.

    Returns:
        G, trianglesIndexMap: The dual graph and a dictionary where the key is the index of the triangle and the value is the triangle itself.
    """
    G = nx.Graph()
    
    trianglesIndexMap = {i: tuple(tuple(vertex) for vertex in triangle) for i, triangle in enumerate(triangles)}

    for i, triangle in trianglesIndexMap.items():
        for j in range(i + 1, len(triangles)):
            diagionalVertices = set(triangle).intersection(set(trianglesIndexMap[j]))
            if len(diagionalVertices) == 2:
                G.add_edge(i, j)
    
    return G, trianglesIndexMap

def plot_colored_polygon(polygon, coloring):
    """"
    Plots the polygon with the given coloring.

    Parameters:
        polygon: A list of vertices.
        coloring: A dictionary where the key is a vertex and the value is a color.

    Returns:
        A Plotly figure with the colored polygon.
    """
    x, y = zip(*polygon)
    colors = [coloring[tuple(vertex)] for vertex in polygon] + [coloring[tuple(polygon[0])]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             marker=dict(color=colors, size=10),
                             line=dict(width=1, color='black'),
                             name='Polygon'))
    fig.update_layout(
        title="Polygon Final Coloring",
        showlegend=True
    )
    return fig

def color_vertices(triangles):
    """
    Colors the vertices of a list of triangles using a DFS algorithm.

    Parameters:
        triangles: A list of triangles, where each triangle is represented as a list of vertices.

    Returns:
        vertexColors: A dictionary where the key is a vertex and the value is a color.
    """
    dual_graph, trianglesIndexMap = create_dual_graph(triangles)
    vertexColors = {}
    colorNames = ['purple', 'green', 'blue']
    visited = set()

    def dfs(index):
        visited.add(index)
        triangle = trianglesIndexMap[index]
        colorSet = set(colorNames)
        
        for vertex in triangle:
            if vertex in vertexColors:
                colorSet.discard(vertexColors[vertex])
        
        for vertex in triangle:
            if vertex not in vertexColors:
                vertexColors[vertex] = colorSet.pop()

        for neighbor in dual_graph.neighbors(index):
            if neighbor not in visited:
                dfs(neighbor)
    
    first = list(dual_graph.nodes)[0]
    dfs(first)
    
    return vertexColors


def animate_colorization(triangles,polygon):
    """
    Animates the colorization of the polygon.

    Parameters:
        triangles: A list of triangles, where each triangle is represented as a list of vertices.
        polygon: A list of vertices.

    Returns:
        frames: A list of Plotly frames
    """
    x, y = zip(*polygon)
    dual_graph, trianglesIndexMap = create_dual_graph(triangles)
    k=0
    vertexColors = {}
    frames = []
    colorNames = ['purple', 'green', 'blue']
    visited = set()
    
    frame_data = [go.Scatter(x=x + (x[0],), y=y + (y[0],), mode='lines+markers', name='Polygon')]
    for indx in dual_graph.nodes:
        x_tri, y_tri = zip(*trianglesIndexMap[indx])
        frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                             mode='lines',fill='toself',fillcolor='rgba(0, 0, 0, 0)', line=dict(width=1, color='black'), 
                                             name='Triangle'))
        
    frames.append(go.Frame(data=frame_data,name=f'frame_{k}'))
    k = k + 1
    def dfs(index):
        nonlocal k
        visited.add(index)
        triangle = trianglesIndexMap[index]
        colorSet = set(colorNames)
        
        
        for vertex in triangle:
            if vertex in vertexColors:
                colorSet.discard(vertexColors[vertex])
        
        frame_data = [go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                mode='lines+markers', 
                name='Polygon')]
        
        
        for indx in dual_graph.nodes:

            if (indx in visited) and (indx != index):
                color = []
                for vertex in trianglesIndexMap[indx]:
                    color = color + [vertexColors[vertex]]
                color = color + [color[0]]
                x_tri, y_tri = zip(*trianglesIndexMap[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='markers',
                            marker=dict(size=10, color=color),
                            fill='toself',)
                            )
                
            elif indx == index:
                x_tri, y_tri = zip(*trianglesIndexMap[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='lines',
                            fill='toself',
                            fillcolor="rgba(0, 0, 0, 0.3)")
                            )
            else:
                x_tri, y_tri = zip(*trianglesIndexMap[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                     mode='lines',fill='toself',fillcolor='rgba(0, 0, 0, 0)',line=dict(width=1, color='black'),
                                     name='Triangle'))
                    
        frames.append(go.Frame(data=frame_data,name=f'frame_{k}'))
        k = k + 1
        
        frame_data = [go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                mode='lines+markers', 
                name='Polygon')]
        
        
        for vertex in triangle:
            if vertex not in vertexColors:
                vertexColors[vertex] = colorSet.pop()
            
        for indx in dual_graph.nodes:

            if (indx in visited) and (indx != index):
                color = []
                for vertex in trianglesIndexMap[indx]:
                    color = color + [vertexColors[vertex]]
                color = color + [color[0]]
                x_tri, y_tri = zip(*trianglesIndexMap[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='markers',
                            marker=dict(size=10, color=color),
                            fill='toself',)
                            )
                
            elif indx == index:
                color = []
                for vertex in trianglesIndexMap[indx]:
                    color = color + [vertexColors[vertex]]
                color = color + [color[0]]
                x_tri, y_tri = zip(*trianglesIndexMap[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='markers',
                            marker=dict(size=10, color=color),
                            fill='toself',
                            fillcolor="rgba(0, 0, 0, 0.3)")
                            )
            else:
                x_tri, y_tri = zip(*trianglesIndexMap[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                     mode='lines', fill='toself',fillcolor='rgba(0, 0, 0, 0)',line=dict(width=1, color='black'),
                                     name='Triangle'))
                    
        
        frames.append(go.Frame(data=frame_data,name=f'frame_{k}'))
        k = k + 1
        for neighbor in dual_graph.neighbors(index):
            if neighbor not in visited:
                dfs(neighbor)
            

    first = list(dual_graph.nodes)[0]
    dfs(first)
    
    return frames

def plot_coloring(polygon,triangles):
    """
    Plots the polygon with the coloring process.

    Parameters:
        polygon: A list of vertices.
        triangles: A list of triangles, where each triangle is represented as a list of vertices.

    Returns:
        A Plotly figure with the coloring process.
    """

    x, y = zip(*polygon)
    fig = go.Figure()
    
    dual_graph, trianglesIndexMap = create_dual_graph(triangles)

    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             marker=dict(size=10, color="black"),
                             name='Polygon'))
    
    for indx in dual_graph.nodes:
        x_tri, y_tri = zip(*trianglesIndexMap[indx])
        fig.add_trace(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                     mode='lines', fill=None,line=dict(width=1, color='black'),
                                     name='Triangle'))
        
    frames = animate_colorization(triangles,polygon)
    
    fig.frames = frames
    fig.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                showactive=True,
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, dict(frame=dict(duration=600, redraw=True), fromcurrent=True, mode='immediate')]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate', transition=dict(duration=0))]
                    )
                ]
            )
        ],
        sliders=[
            dict(
                steps=[
                    dict(
                        method='animate',
                        args=[
                            [f'frame_{k}'],
                            dict(
                                mode='immediate',
                                frame=dict(duration=2000, redraw=True),
                                transition=dict(duration=0)
                            )
                        ],
                        label=f'Slide {k+1}'
                    ) for k in range(len(frames))
                ],
                active=0,
                transition=dict(duration=0),
                currentvalue=dict(font=dict(size=12), visible=True, xanchor='center')
            )
        ],
        xaxis=dict(range=[min(x) - 1, max(x) + 1]),
        yaxis=dict(range=[min(y) - 1, max(y) + 1]),
    )

    

    fig.update_layout(
        title="Polygon Coloring",
        showlegend=True
    )
    return fig
