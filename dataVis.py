import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from data import getDatasFromTDFFinishers, getDatasFromTDFStages, getDatasFromTDFTours
from data import graphNumberOfFinisher, graphAverageSpeed, graphTimeOfFirst, graphMultilineTimeOfFirst

# Créer une instance de l'application Dash
app = dash.Dash(__name__)

dfFinishers = getDatasFromTDFFinishers()
dfStages = getDatasFromTDFStages()
dfTours = getDatasFromTDFTours()
startYear = 1903
endYear = 2022
compareStarters = False

# Définir la disposition de l'application
app.layout = html.Div(children=[
    html.H1(children='Data Visualisation Application'),
    
    # Graphique pour le rapport finishers / starters
    html.H2(children='Ratio Finishers / Starters by year graph'),
    
    html.Div(children='''
        Select year start to display the number of finishers:
    '''),
    dcc.Input(id='start-year-input', type='number', value=1903, min=1903, max=2022),
    
    html.Div(children='''
        Select year end to display the number of finishers:
    '''),
    dcc.Input(id='end-year-input', type='number', value=2021, min=1903, max=2022),
    
    html.Div(children='Show Finishers:'),
    dcc.Checklist(
        id='show-finishers-checklist',
        options=[
            {'label': 'Show Starters', 'value': 'show_starters'},
        ],
        value=[],
        labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Graph(
        id='finisher-graph'
    ),
    
    # Graphique pour la vitesse moyenne
    html.H2(children='Average speed by year graph'),
    
    html.Div(children='''
        Select year start to display the number of finishers:
    '''),
    dcc.Input(id='start-year-input_avgspeed', type='number', value=1903, min=1903, max=2022),
    
    html.Div(children='''
        Select year end to display the number of finishers:
    '''),
    dcc.Input(id='end-year-input_avgspeed', type='number', value=2021, min=1903, max=2022),
    
    dcc.Graph(
        id='avgspeed-graph'
    ),
    
    # Graphique pour le temps des premiers
    html.H2(children='Compare time of first riders for a year bar graph'),
    
    html.Div(children='''
        Select year to display :
    '''),
    dcc.Input(id='yearToDisplay-input', type='number', value=1903, min=1903, max=2022),
    
    html.Div(children='''
        Select riders to display:
    '''),

    dcc.Dropdown(
        id='timeOfFirsts-dropdown',
        options=[
            {'label': 'First Rider', 'value': 'first_rider'},
            {'label': 'Second Rider', 'value': 'second_rider'},
            {'label': 'Third Rider', 'value': 'third_rider'}
        ],
        value=['first_rider', 'second_rider', 'third_rider'],
        multi=True
    ),
    
    html.Div(children='''
        Select time ladder:
    '''),
    
    dcc.Dropdown(
        id='time_Ladder-dropdown',
        options=[
            {'label': 'Hour', 'value': 'hour'},
            {'label': 'Minute', 'value': 'minute'},
            {'label': 'Second', 'value': 'second'}
        ],
        value='hour',
        multi=False
    ),

    dcc.Graph(
        id='timeOfFirsts-graph'
    ),
    
    # Graphique pour l'écart entre les 3 premiers'
    html.H2(children='Compare time of first riders by year multiline graph'),
    
    html.Div(children='''
        Select year start to display:
    '''),
    dcc.Input(id='start_year-input', type='number', value=1903, min=1903, max=2022),
    
    html.Div(children='''
        Select year end to display:
    '''),
    dcc.Input(id='end_year-input', type='number', value=2021, min=1903, max=2022),
    
    html.Div(children='''
        Select time ladder:
    '''),
    
    dcc.Dropdown(
        id='timeLadder-dropdown',
        options=[
            {'label': 'Hour', 'value': 'hour'},
            {'label': 'Minute', 'value': 'minute'},
            {'label': 'Second', 'value': 'second'}
        ],
        value='hour',
        multi=False
    ),

    dcc.Graph(
        id='multilineFirsts-graph'
    ),
    
    html.Button('Reset Zoom', id='reset-zoom-button', n_clicks=0)
])


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
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        hovermode='closest',
        dragmode='zoom',
    )
    return fig

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
