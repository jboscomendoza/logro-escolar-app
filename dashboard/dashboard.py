import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
#from .dashboard_layout import html_layout


datos = [{
        'x': ["a", "b", "c"],
        'y': [1, 2, 3],
        'name': 'bar-plot',
        'type': 'bar'
    }]



def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/',
        #external_stylesheets=['../static/css/main.css']
    )
    # Custom HTML layout
    #dash_app.index_string = html_layout
    # Create Layout

    dash_app.layout = html.Div(children=[
        html.H1(children="Hola amigos"),
        html.Div([
            dcc.Graph(
                id='bar-plot',
                figure={
                    'data': datos,
                    'layout': {
                        'title': 'Bar plot'
                    }
                },
                style={
                        'display': 'block'
                },
            )
        ])
    ])
    return dash_app.server

