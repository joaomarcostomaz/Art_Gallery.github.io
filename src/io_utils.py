import pandas as pd
import os
import base64
import io
import json



def read_polygon_from_file(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', file_name)
    print(f"Loading polygon from file: {file_path}")

    df = pd.read_csv(file_path, header=None)
    polygon = df.values.tolist()
    return polygon

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).replace(b'\n', b' ')


    if filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)

        df = df.drop(0)
        df.iloc[:, :] = df.iloc[:, :].astype(float)
        polygon = df.values.tolist()
    elif filename.endswith('.txt'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None, delimiter='\t')
        df = df.drop(0)
        df.iloc[:, :] = df.iloc[:, :].astype(float)
        polygon = df.values.tolist()
    elif filename.endswith('.pol'):
        data = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None, sep='\s+').T
        polygon = []

        if(len(data[0]) > 2):
            for i in range(1, len(data[0]), 2):
                x_fracao = str(data.iloc[i,0]).split('/')
                y_fracao = str(data.iloc[i + 1,0]).split('/')
                
                x = float(x_fracao[0]) / float(x_fracao[1])
                y = float(y_fracao[0]) / float(y_fracao[1])
                polygon.append([x, y])   
        else:
            for i in range(0, data.shape[1]):
                x_fracao = str(data.iloc[0, i]).split('/')
                y_fracao = str(data.iloc[1, i]).split('/')     
                x = float(x_fracao[0]) / float(x_fracao[1])
                y = float(y_fracao[0]) / float(y_fracao[1])
                polygon.append([x, y])
    else:
        return None
    return polygon

def parse_manual_input(input_string):
    try:
        lines = input_string.strip().split('\n')
        polygon = [list(map(float, line.split(','))) for line in lines]
        return polygon
    except ValueError:
        return None