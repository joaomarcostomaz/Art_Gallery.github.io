import networkx as nx

def color_vertices(triangles):
    G = nx.Graph()
    for triangle in triangles:
        for i in range(3):
            for j in range(i+1, 3):
                G.add_edge(tuple(triangle[i]), tuple(triangle[j]))
    
    coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    return coloring

def minimum_camera_positions(triangles):
    G = nx.Graph()
    for triangle in triangles:
        for i in range(3):
            for j in range(i + 1, 3):
                G.add_edge(tuple(triangle[i]), tuple(triangle[j]))

    coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    max_color = max(coloring.values()) + 1
    cameras = [[] for _ in range(max_color)]

    for vertex, color in coloring.items():
        cameras[color].append(vertex)

    camera_positions = [list(group[0]) for group in cameras if group] 
    return camera_positions
