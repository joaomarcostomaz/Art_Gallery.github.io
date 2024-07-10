import numpy as np
import pandas as pd
import random

def generate_convex_polygon(num_sides):
    angles = sorted([random.uniform(0, 2 * np.pi) for _ in range(num_sides)])
    radius = 10
    points = [(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles]
    return points

def generate_random_polygon(num_sides):
    points = []
    for _ in range(num_sides):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        points.append((x, y))
    return points

def generate_polygon_csv(num_sides, convex=True):
    if convex:
        polygon_points = generate_convex_polygon(num_sides)
    else:
        polygon_points = generate_random_polygon(num_sides)
    
    df = pd.DataFrame(polygon_points, columns=['x', 'y'])
    file_path = f'{num_sides}_sided_polygon_{"convex" if convex else "random"}.csv'
    df.to_csv(file_path, index=False)
    
    print(f"{num_sides}-sided {'convex' if convex else 'random'} polygon CSV file generated: {file_path}")
    return file_path

generate_polygon_csv(50, convex=True)
generate_polygon_csv(20, convex=False) 

