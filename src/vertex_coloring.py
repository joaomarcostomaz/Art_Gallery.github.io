import networkx as nx
import plotly.graph_objects as go


def create_dual_graph(triangles):
    G = nx.Graph()
    
    index_to_triangle = {i: tuple(tuple(vertex) for vertex in triangle) for i, triangle in enumerate(triangles)}

    for i, triangle in index_to_triangle.items():
        for j in range(i + 1, len(triangles)):
            diagionalVertices = set(triangle).intersection(set(index_to_triangle[j]))
            if len(diagionalVertices) == 2:
                G.add_edge(i, j)
    
    return G, index_to_triangle

def color_vertices(triangles):
    dual_graph, index_to_triangle = create_dual_graph(triangles)
    vertexColors = {}
    colorNames = ['purple', 'green', 'blue']
    visited = set()

    def dfs(index):
        visited.add(index)
        triangle = index_to_triangle[index]
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



def minimum_camera_positions(triangles):
    vertexColors = color_vertices(triangles)
    
    colorPartitions = {'purple': [], 'green': [], 'blue': []}
    for vertex, color in vertexColors.items():
        colorPartitions[color].append(vertex)
    
    smallestPartition = min(colorPartitions.values(), key=len)
    cameraPositions = list(set(smallestPartition))
    
    return cameraPositions

def animate_colorization(triangles,polygon):
    x, y = zip(*polygon)
    dual_graph, index_to_triangle = create_dual_graph(triangles)
    vertexColors = {}
    frames = []
    colorNames = ['purple', 'green', 'blue']
    visited = set()

    def dfs(index):
        visited.add(index)
        triangle = index_to_triangle[index]
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
                for vertex in index_to_triangle[indx]:
                    color = color + [vertexColors[vertex]]
                color = color + [color[0]]
                print(color)
                x_tri, y_tri = zip(*index_to_triangle[indx])
                print(x_tri + (x_tri[0],))
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='markers',
                            marker=dict(size=10, color=color),
                            fill=None,
                            fillcolor="rgba(0, 0, 0, 0.3)")
                            )
                
            elif indx == index:
                x_tri, y_tri = zip(*index_to_triangle[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='lines',
                            fill='toself',
                            fillcolor="rgba(0, 0, 0, 0.3)")
                            )
            else:
                x_tri, y_tri = zip(*index_to_triangle[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                     mode='lines', fill=None,line=dict(width=1, color='black'),
                                     name='Triangle'))
                    
        frames.append(go.Frame(data=frame_data))
        
        frame_data = [go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                mode='lines+markers', 
                name='Polygon')]
        
        
        for vertex in triangle:
            if vertex not in vertexColors:
                vertexColors[vertex] = colorSet.pop()
            
        for indx in dual_graph.nodes:

            if (indx in visited) and (indx != index):
                color = []
                for vertex in index_to_triangle[indx]:
                    color = color + [vertexColors[vertex]]
                color = color + [color[0]]
                x_tri, y_tri = zip(*index_to_triangle[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='markers',
                            marker=dict(size=10, color=color),
                            fill=None,
                            fillcolor="rgba(0, 0, 0, 0.3)")
                            )
                
            elif indx == index:
                color = []
                for vertex in index_to_triangle[indx]:
                    color = color + [vertexColors[vertex]]
                color = color + [color[0]]
                x_tri, y_tri = zip(*index_to_triangle[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                            mode='markers',
                            marker=dict(size=10, color=color),
                            fill='toself',
                            fillcolor="rgba(0, 0, 0, 0.3)")
                            )
            else:
                x_tri, y_tri = zip(*index_to_triangle[indx])
                frame_data.append(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                     mode='lines', fill=None,line=dict(width=1, color='black'),
                                     name='Triangle'))
                    
        
        frames.append(go.Frame(data=frame_data))
        for neighbor in dual_graph.neighbors(index):
            if neighbor not in visited:
                dfs(neighbor)
            

    first = list(dual_graph.nodes)[0]
    dfs(first)
    
    return frames

def plot_coloring(polygon,triangles):
    x, y = zip(*polygon)
    fig = go.Figure()
    
    dual_graph, index_to_triangle = create_dual_graph(triangles)

    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), 
                             mode='lines+markers', 
                             marker=dict(size=10, color="black"),
                             name='Polygon'))
    
    for indx in dual_graph.nodes:
        x_tri, y_tri = zip(*index_to_triangle[indx])
        fig.add_trace(go.Scatter(x=x_tri + (x_tri[0],), y=y_tri + (y_tri[0],), 
                                     mode='lines', fill=None,line=dict(width=1, color='black'),
                                     name='Triangle'))
        
    frames = animate_colorization(triangles,polygon)
    
    fig.frames = frames
    fig.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=True,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=1000, redraw=True), 
                                 fromcurrent=True, mode='immediate')]
            )]
        )],
        xaxis=dict(range=[min(x) - 1, max(x) + 1]),
        yaxis=dict(range=[min(y) - 1, max(y) + 1])
    ),
    

    fig.update_layout(
        title="Triangle",
        showlegend=False
    )
    return fig
