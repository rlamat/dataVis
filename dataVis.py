import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from data import getDatasFromTDFFinishers, getDatasFromTDFStages, getDatasFromTDFTours
from data import graphNumberOfFinisher, graphAverageSpeed, graphTimeOfFirst, graphMultilineTimeOfFirst, graphTheAverageBetweenStartersAndFinishers

# Créer une instance de l'application Dash
app = dash.Dash(__name__)
app.title = 'Tour de France Data Visualization'
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

dfFinishers = getDatasFromTDFFinishers()
dfStages = getDatasFromTDFStages()
dfTours = getDatasFromTDFTours()
startYear = 1903
endYear = 2022
compareStarters = False

# Définir la disposition de l'application
app.layout = html.Div(
    style={'margin': '0 auto', 'padding': '10px', 'maxWidth': '1000px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1('Tour de France Data Visualization', style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div([
            html.H2('Ratio Finishers / Starters by Year', style={'textAlign': 'center'}),
            html.Div([
                html.Label('Select year start:', style={'marginRight': '10px'}),
                dcc.Input(id='start-year-input', type='number', value=1903, min=1903, max=2022)
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Select year end:', style={'marginRight': '10px'}),
                dcc.Input(id='end-year-input', type='number', value=2021, min=1903, max=2022)
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Show Starters:', style={'marginRight': '10px'}),
                dcc.Checklist(
                    id='show-finishers-checklist',
                    options=[{'label': 'Show Starters', 'value': 'show_starters'}],
                    value=[],
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'marginBottom': '20px'}),
            
            dcc.Graph(id='finisher-graph'),
            dcc.Graph(id='average-between-starters-and-finishers')
        ], style={'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '10px', 'marginBottom': '20px'}),
        
        html.Div([
            html.H2('Average Speed by Year', style={'textAlign': 'center'}),
            html.Div([
                html.Label('Select year start:', style={'marginRight': '10px'}),
                dcc.Input(id='start-year-input_avgspeed', type='number', value=1903, min=1903, max=2022)
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Select year end:', style={'marginRight': '10px'}),
                dcc.Input(id='end-year-input_avgspeed', type='number', value=2021, min=1903, max=2022)
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            
            dcc.Graph(id='avgspeed-graph')
        ], style={'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '10px', 'marginBottom': '20px'}),
        
        html.Div([
            html.H2('Time of First Riders for a Year', style={'textAlign': 'center'}),
            html.Div([
                html.Label('Select year:', style={'marginRight': '10px'}),
                dcc.Input(id='yearToDisplay-input', type='number', value=1903, min=1903, max=2022)
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Select riders:', style={'marginRight': '10px'}),
                dcc.Dropdown(
                    id='timeOfFirsts-dropdown',
                    options=[
                        {'label': 'First Rider', 'value': 'first_rider'},
                        {'label': 'Second Rider', 'value': 'second_rider'},
                        {'label': 'Third Rider', 'value': 'third_rider'}
                    ],
                    value=['first_rider', 'second_rider', 'third_rider'],
                    multi=True,
                    style={'minWidth': '200px'}
                )
            ], style={'marginBottom': '10px'}),
            
            html.Div([
                html.Label('Select time ladder:', style={'marginRight': '10px'}),
                dcc.Dropdown(
                    id='time_Ladder-dropdown',
                    options=[
                        {'label': 'Hour', 'value': 'hour'},
                        {'label': 'Minute', 'value': 'minute'},
                        {'label': 'Second', 'value': 'second'}
                    ],
                    value='hour',
                    multi=False,
                    style={'minWidth': '200px'}
                )
            ], style={'marginBottom': '20px'}),
            
            dcc.Graph(id='timeOfFirsts-graph')
        ], style={'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '10px', 'marginBottom': '20px'}),
        
        html.Div([
            html.H2('Compare Time of First Riders by Year', style={'textAlign': 'center'}),
            html.Div([
                html.Label('Select year start:', style={'marginRight': '10px'}),
                dcc.Input(id='start_year-input', type='number', value=1903, min=1903, max=2022)
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Select year end:', style={'marginRight': '10px'}),
                dcc.Input(id='end_year-input', type='number', value=2021, min=1903, max=2022)
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Select time ladder:', style={'marginRight': '10px'}),
                dcc.Dropdown(
                    id='timeLadder-dropdown',
                    options=[
                        {'label': 'Hour', 'value': 'hour'},
                        {'label': 'Minute', 'value': 'minute'},
                        {'label': 'Second', 'value': 'second'}
                    ],
                    value='hour',
                    multi=False,
                    style={'minWidth': '200px'}
                )
            ], style={'marginBottom': '20px'}),
            
            dcc.Graph(id='multilineFirsts-graph')
        ], style={'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '10px', 'marginBottom': '20px'}),
        
        html.Button('Reset Zoom', id='reset-zoom-button', n_clicks=0, style={'display': 'block', 'margin': '0 auto'})
    ]
)


@app.callback(
    Output('finisher-graph', 'figure'),
    [Input('start-year-input', 'value'),
     Input('end-year-input', 'value'),
     Input('show-finishers-checklist', 'value')]
)
def update_finisher_graph(start_year, end_year, show_finishers_checklist):
    show_finishers = 'show_starters' in show_finishers_checklist
    fig = graphNumberOfFinisher(dfTours, start_year, end_year, show_finishers)
    return fig


@app.callback(
    Output('avgspeed-graph', 'figure'),
    [Input('start-year-input_avgspeed', 'value'),
     Input('end-year-input_avgspeed', 'value')]
)
def update_avgspeed_graph(start_year, end_year):
    fig = graphAverageSpeed(dfFinishers, dfTours, start_year, end_year)
    return fig


@app.callback(
    Output('timeOfFirsts-graph', 'figure'),
    Input('timeOfFirsts-dropdown', 'value'),
    Input('yearToDisplay-input', 'value'),
    Input('time_Ladder-dropdown', 'value')
)
def update_timeOfFirsts_graph(selected_riders, yearToDisplay, time_ladder):
    firstRider = False
    secondRider = False
    thirdRider = False
    if 'first_rider' in selected_riders:
        firstRider = True
    if 'second_rider' in selected_riders:
        secondRider = True
    if 'third_rider' in selected_riders:
        thirdRider = True
    fig = graphTimeOfFirst(dfFinishers, yearToDisplay, firstRider, secondRider, thirdRider, time_ladder)
    return fig

@app.callback(
    Output('multilineFirsts-graph', 'figure'),
    [Input('start_year-input', 'value'),
     Input('end_year-input', 'value'),
     Input('reset-zoom-button', 'n_clicks'),
     Input('timeLadder-dropdown', 'value')]
)
def update_multilineFirsts_graph(start_year, end_year, n_clicks, time_ladder):
    fig = graphMultilineTimeOfFirst(dfFinishers, start_year, end_year, time_ladder)
    fig.update_layout(
        title='Graphique interactif avec zoom',
        xaxis_title='Year',
        yaxis_title='Time',
        hovermode='closest',
        dragmode='zoom',
    )
    return fig

@app.callback(
    Output('average-between-starters-and-finishers', 'figure'),
    [Input('start-year-input', 'value'),
     Input('end-year-input', 'value')]
)
def update_average_between_starters_and_finishers(start_year, end_year):
    fig = graphTheAverageBetweenStartersAndFinishers(dfTours, start_year, end_year)
    return fig

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
