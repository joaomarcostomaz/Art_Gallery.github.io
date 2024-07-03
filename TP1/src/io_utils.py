import pandas as pd
import os

def read_polygon_from_file(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', file_name)
    print(f"Loading polygon from file: {file_path}")

    df = pd.read_csv(file_path, header=None)
    polygon = df.values.tolist()
    return polygon
