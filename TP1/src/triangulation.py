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
    
