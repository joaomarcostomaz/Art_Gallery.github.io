import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import json
import src.plotting as plotting
import src.triangulation as triangulation
import src.vertex_coloring as vertex_coloring
from dash.exceptions import PreventUpdate

print("Initializing the Dash app")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("ART GALLERY PROBLEM"), width={"size": 8, "offset": 2}),
    ], justify="center"),
    
    
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-polygon',
                children=dbc.Button("Drag and Drop or Select a Polygon File", color="primary", className="w-100"),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
                multiple=False
            ),
            dcc.Textarea(
                id='manual-polygon-input',
                placeholder='Enter polygon points as x,y pairs, one per line',
                style={'width': '100%', 'height': '100px', 'margin-top': '10px'}
            ),
            dbc.Button('Submit Points', id='submit-points-button', color="secondary", className="w-100", style={'margin-top': '10px'}),
            dbc.Button('Triangulate', id='triangulate-button', color="info", className="w-100", style={'margin-top': '10px'}),
            dbc.Button('Final Triangulation', id='final-triangulate-button', color="info", className="w-100", style={'margin-top': '10px'}),
            dbc.Button('Color Vertices', id='color-button', color="warning", className="w-100", style={'margin-top': '10px'}),
            dbc.Button('Cameras', id='camera-button', color="danger", className="w-100", style={'margin-top': '10px'}),
            dcc.Store(id='polygon-data'),
            dcc.Store(id='triangles-data'),
            dcc.Store(id='final-triangulate-data'),
            dcc.Store(id='coloring-data'),
            dcc.Store(id='camera-data'),
            dcc.ConfirmDialog(
                id='file-type-dialog',
                message='Invalid file type. Please upload a CSV, TXT or POL file.'
            ),
            html.Div(id='camera-output', style={'margin-top': '20px'})
        ], width={"size": 4}),
        
        dbc.Col([
            dcc.Graph(id='polygon-graph')
        ], width={"size": 8})
    ]),
], style={'backgroundColor': '#e6f2ff'})

print("Layout set up")

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)


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
    print(polygon)
    return polygon

def parse_manual_input(input_string):
    try:
        lines = input_string.strip().split('\n')
        polygon = [list(map(float, line.split(','))) for line in lines]
        return polygon
    except ValueError:
        return None

@app.callback(
    Output('file-type-dialog', 'displayed'),
    Output('polygon-data', 'data'),
    Output('triangles-data', 'data'),
    Output('coloring-data', 'data'),
    Output('camera-data', 'data'),
    Output('polygon-graph', 'figure'),
    Output('camera-output', 'children'),
    Input('upload-polygon', 'contents'),
    Input('submit-points-button', 'n_clicks'),
    Input('triangulate-button', 'n_clicks'),
    Input('final-triangulate-button', 'n_clicks'),
    Input('color-button', 'n_clicks'),
    Input('camera-button', 'n_clicks'),
    State('upload-polygon', 'filename'),
    State('manual-polygon-input', 'value'),
    State('polygon-data', 'data'),
    State('triangles-data', 'data'),
    State('coloring-data', 'data'),
    State('camera-data', 'data')
)
def update_graph(contents, submit_points_clicks, triangulate_clicks,final_triangles_clicks, color_clicks, camera_clicks, filename, manual_input, polygon, triangles, coloring, camera_data):
    ctx = callback_context
    if not ctx.triggered:
        return False, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Button {button_id} clicked")

    if button_id == 'upload-polygon' and contents:
        print("entrei")
        polygon = parse_contents(contents, filename)
        if polygon is None:
            return True, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        fig = plotting.plot_polygon(polygon)
        return False, polygon,dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update

    if button_id == 'submit-points-button' and submit_points_clicks > 0:
        polygon = parse_manual_input(manual_input)
        if polygon is None:
            return True, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        fig = plotting.plot_polygon(polygon)
        return False, polygon,dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update

    if button_id == 'triangulate-button' and triangulate_clicks > 0 and polygon:
        if not triangles:
            triangles = triangulation.ear_clipping_triangulation(polygon)        
        fig = plotting.plot_test(polygon)
        return False, polygon, triangles,dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update
    
    if button_id == 'final-triangulate-button' and final_triangles_clicks > 0 and polygon:
        if not triangles:
            triangles = triangulation.ear_clipping_triangulation(polygon)        
        fig = plotting.animate_triangulation(polygon,triangles)
        return False, polygon, triangles,dash.no_update, dash.no_update, fig, dash.no_update

    if button_id == 'color-button' and color_clicks > 0 and polygon:
        if not triangles:
            triangles = triangulation.ear_clipping_triangulation(polygon)
        coloring = vertex_coloring.color_vertices(triangles)
        coloring_serializable = {str(k): v for k, v in coloring.items()}
        print(coloring)
        fig = plotting.plot_colored_polygon(polygon, coloring)
        return False, polygon,triangles, coloring_serializable, dash.no_update, fig, dash.no_update

    if button_id == 'camera-button' and camera_clicks > 0 and polygon:
        if not triangles:
            triangles = triangulation.ear_clipping_triangulation(polygon)
        if not coloring:
            coloring = vertex_coloring.color_vertices(triangles)
        camera_positions = vertex_coloring.minimum_camera_positions(triangles)
        fig = plotting.animate_cameras(polygon, camera_positions)
        num_cameras = len(camera_positions)
        camera_message = dbc.Alert(
            f'Minimum number of cameras needed: {num_cameras}', color="info", style={'margin-top': '20px'}
        )
        return False, polygon,triangles, coloring, camera_positions, fig, camera_message

    return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update

if __name__ == '__main__':
    print("Starting the Dash app server...")
    app.run_server(debug=True)
