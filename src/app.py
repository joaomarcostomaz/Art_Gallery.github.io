import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import src.plotting as plotting
import src.triangulation as triangulation
import src.cameras as cameras
import src.vertex_coloring as vertex_coloring
from src.io_utils import parse_contents,parse_manual_input
import os

print("Initializing the Dash app")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(fluid=True,children=[
    dbc.Row([
        dbc.Col(html.H1("ART GALLERY PROBLEM",style={"margin-bottom": "40px","margin-top": "20px"}), width={"size": 8, "offset": 2}),
    ], justify="center"),
    
    
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-polygon',
                children=dbc.Button("Drag and Drop or Select a Polygon File", color="secondary", className="w-100"),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    "margin-left": "30px",
                },
                multiple=False
            ),
            dcc.Textarea(
                id='manual-polygon-input',
                placeholder='Enter polygon points as x,y pairs, one per line',
                style={'width': '100%', 'height': '100px', 'margin-top': '10px',"margin-left": "30px",}
            ),
            dbc.Button('Submit Points', id='submit-points-button', color="secondary", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dbc.Button('See polygon', id='see-polygon-button', color="primary", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dbc.Button('Triangulate', id='triangulate-button', color="info", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dbc.Button('Final Triangulation', id='final-triangulate-button', color="info", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dbc.Button('Color Vertices', id='color-button', color="warning", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dbc.Button('Final Coloring', id='final-coloring-button', color="warning", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dbc.Button('Cameras', id='camera-button', color="danger", className="w-100", style={'margin-top': '10px',"margin-left": "30px",}),
            dcc.Store(id='polygon-data'),
            dcc.Store(id='see-polygon-data'),
            dcc.Store(id='triangles-data'),
            dcc.Store(id='final-triangulate-data'),
            dcc.Store(id='final-coloring-data'),
            dcc.Store(id='coloring-data'),
            dcc.Store(id='camera-data'),
            dcc.ConfirmDialog(
                id='file-type-dialog',
                message='Invalid file type. Please upload a CSV, TXT or POL file.'
            ),
            html.Div(id='camera-output', style={'margin-top': '20px',"margin-left": "30px",})
        ], width={"size": 3}),
        
        dbc.Col([
            dcc.Graph(id='polygon-graph',style={'margin-top': '30px',"margin-left": "50px",})
        ], width={"size": 9})
    ]),
], style={'backgroundColor': '#e6f2ff'})

print("Layout set up")

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
    Input('see-polygon-button', 'n_clicks'),
    Input('triangulate-button', 'n_clicks'),
    Input('final-triangulate-button', 'n_clicks'),
    Input('color-button', 'n_clicks'),
    Input('final-coloring-button', 'n_clicks'),
    Input('camera-button', 'n_clicks'),
    
    State('upload-polygon', 'filename'),
    State('manual-polygon-input', 'value'),
    State('polygon-data', 'data'),
    State('triangles-data', 'data'),
    State('coloring-data', 'data'),
    State('camera-data', 'data')
)
def update_graph(contents, submit_points_clicks,see_polygon_clicks, triangulate_clicks,final_triangles_clicks, color_clicks,final_coloring_clicks, camera_clicks, filename, manual_input, polygon, triangles, coloring, camera_data):
    ctx = callback_context
    if not ctx.triggered:
        return False, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Button {button_id} clicked")


    if button_id == 'upload-polygon' and contents:
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

    if button_id == 'see-polygon-button' and see_polygon_clicks > 0:
        if polygon is None:
            return True, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        fig = plotting.plot_polygon(polygon)

        path = f"data/polygon-{len(polygon)}"
        if not os.path.exists(path):
            os.makedirs(path)

        fig.write_html(f"{path}/polygon.html", full_html=False, include_plotlyjs='cdn', auto_play=False)
        
        return False, polygon,dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update

    if button_id == 'triangulate-button' and triangulate_clicks > 0 and polygon:
        triangles = triangulation.ear_clipping_triangulation(polygon)        
        fig = triangulation.plot_triangulation(polygon)

        path = f"data/polygon-{len(polygon)}"
        if not os.path.exists(path):
            os.makedirs(path)
            
        fig.write_html(f"{path}/triangulation.html", full_html=False, include_plotlyjs='cdn', auto_play=False)

        return False, polygon,triangles,dash.no_update, dash.no_update, fig, dash.no_update
    
    if button_id == 'final-triangulate-button' and final_triangles_clicks > 0 and polygon:
        triangles = triangulation.ear_clipping_triangulation(polygon)        
        fig = triangulation.plot_triangles_static(polygon,triangles)

        path = f"data/polygon-{len(polygon)}"
        if not os.path.exists(path):
            os.makedirs(path)
            
        fig.write_html(f"{path}/final-triangulation.html", full_html=False, include_plotlyjs='cdn', auto_play=False)

        return False, polygon, triangles,dash.no_update, dash.no_update, fig, dash.no_update

    if button_id == 'color-button' and color_clicks > 0 and polygon:
        triangles = triangulation.ear_clipping_triangulation(polygon)
        coloring = vertex_coloring.color_vertices(triangles)
        coloring_serializable = {str(k): v for k, v in coloring.items()}
        fig = vertex_coloring.plot_coloring(polygon,triangles)
        
        path = f"data/polygon-{len(polygon)}"
        if not os.path.exists(path):
            os.makedirs(path)
            
        fig.write_html(f"{path}/coloring.html", full_html=False, include_plotlyjs='cdn', auto_play=False)

        return False, polygon,triangles, coloring_serializable, dash.no_update, fig, dash.no_update

    if button_id == 'final-coloring-button' and final_coloring_clicks > 0 and polygon:
        triangles = triangulation.ear_clipping_triangulation(polygon)
        coloring = vertex_coloring.color_vertices(triangles)
        coloring_serializable = {str(k): v for k, v in coloring.items()}
        fig = vertex_coloring.plot_colored_polygon(polygon, coloring)
        
        path = f"data/polygon-{len(polygon)}"
        if not os.path.exists(path):
            os.makedirs(path)
            
        fig.write_html(f"{path}/final-coloring.html", full_html=False, include_plotlyjs='cdn', auto_play=False)

        return False, polygon,triangles, coloring_serializable, dash.no_update, fig, dash.no_update

    if button_id == 'camera-button' and camera_clicks > 0 and polygon:
        triangles = triangulation.ear_clipping_triangulation(polygon)
        coloring = vertex_coloring.color_vertices(triangles)
        coloring_serializable = {str(k): v for k, v in coloring.items()}
        camera_positions = cameras.minimum_camera_positions(triangles)
        fig = cameras.animate_cameras(polygon, camera_positions)

        path = f"data/polygon-{len(polygon)}"
        if not os.path.exists(path):
            os.makedirs(path)
            
        fig.write_html(f"{path}/cameras.html", full_html=False, include_plotlyjs='cdn', auto_play=False)

        num_cameras = len(camera_positions)
        camera_message = dbc.Alert(
            f'Minimum number of cameras needed: {num_cameras}', color="info", style={'margin-top': '20px'}
        )
        return False, polygon,triangles, coloring_serializable, camera_positions, fig, camera_message

    return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update

if __name__ == '__main__':
    print("Starting the Dash app server...")
    app.run_server(debug=True,port=8051)
