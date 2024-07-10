import networkx as nx

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
    colorNames = ['white', 'black', 'gray']
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
    
    colorPartitions = {'white': [], 'black': [], 'gray': []}
    for vertex, color in vertexColors.items():
        colorPartitions[color].append(vertex)
    
    smallestPartition = min(colorPartitions.values(), key=len)
    cameraPositions = list(set(smallestPartition))
    
    return cameraPositions

# Exemplo de uso (ignora isso aqui):
# polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]  # Exemplo de polígono quadrado
# Você precisará definir a função `triangulate_polygon` ou usar uma biblioteca
# para obter os triângulos para o polígono dado.
# camera_positions = minimum_camera_positions(polygon)
# print(camera_positions)
