import datetime

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly
from get_data import get_map_data, plot

# pip install pyorbital

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css']
get_map_data()
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Warthunder Map Rotation'),
        #html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*10000, # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='update-sheet',
            interval=1*60000, # in milliseconds
            n_intervals=0
        )
    ])
)



# Multiple components can update everytime interval gets fired.
@callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    return plot()

@callback(Input('update-sheet', 'n_intervals'))
def update_graph_live(n):
    get_map_data()




if __name__ == '__main__':
    app.run(debug=True)