import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from data import getDatasFromTDFFinishers, getDatasFromTDFStages, getDatasFromTDFTours
from data import graphNumberOfFinisher, graphAverageSpeed, graphTimeOfFirst, graphMultilineTimeOfFirst, graphTheAverageBetweenStartersAndFinishers

# Créer une instance de l'application Dash
app = dash.Dash(__name__)
app.title = "Data Visualisation Application"
server = app.server

dfFinishers = getDatasFromTDFFinishers()
dfStages = getDatasFromTDFStages()
dfTours = getDatasFromTDFTours()
startYear = 1903
endYear = 2022
compareStarters = False

# Définir la disposition de l'application avec des onglets pour les graphiques
app.layout = html.Div(children=[
    html.H1(children='Data Visualisation of Tour de France', style={'textAlign': 'center', 'color': 'white'}),
    
    dcc.Tabs(id="tabs-example", value='tab-1', children=[
        dcc.Tab(label='Ratio Finishers / Starters', value='tab-1', style={'color': 'black'}),
        dcc.Tab(label='Average Speed', value='tab-2', style={'color': 'black'}),
        dcc.Tab(label='Time of First Riders', value='tab-3', style={'color': 'black'}),
        dcc.Tab(label='Multiline Time of First Riders', value='tab-4', style={'color': 'black'}),
    ], style={'background': '#1a1a1a', 'color': 'white'}),
    
    html.Div(id='tabs-content-example')
], style={'backgroundImage': 'url("https://www.tourisme-couserans-pyrenees.com/wp-content/uploads/2023/10/image00004-siteweb-500K-1480x630.jpg")', 'backgroundSize': 'cover','backgroundRepeat' : 'no-repeat' ,'opacity': 0.8})

@app.callback(Output('tabs-content-example', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H2('Ratio Finishers / Starters by year graph', style={'color': 'white'}),
            html.Div('Select year start to display the number of finishers:', style={'color': 'white'}),
            dcc.Input(id='start-year-input', type='number', value=1903, min=1903, max=2022),
            html.Div('Select year end to display the number of finishers:', style={'color': 'white'}),
            dcc.Input(id='end-year-input', type='number', value=2021, min=1903, max=2022),
            html.Div('Show Finishers:', style={'color': 'white'}),
            dcc.Checklist(
                id='show-finishers-checklist',
                options=[{'label': 'Show Starters', 'value': 'show_starters'}],
                value=[], labelStyle={'display': 'inline-block', 'color': 'white'}
            ),
            dcc.Graph(id='finisher-graph'),
            
            html.Div([
                html.Label('Select year start:', style={'marginRight': '10px', 'color': 'white', 'marginBottom': '15px'}),
                dcc.Input(id='start-year-input2', type='number', value=1903, min=1903, max=2022)  # Vérifiez cet ID
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Label('Select year end:', style={'marginRight': '10px', 'color': 'white',, 'marginBottom': '15px'}),
                dcc.Input(id='end-year-input2', type='number', value=2021, min=1903, max=2022)  # Vérifiez cet ID
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
            
            dcc.Graph(id='average-between-starters-and-finishers')
            
        ], style={'padding': '20px', 'animation': 'fade-in 1s'}),

    elif tab == 'tab-2':
        return html.Div([
            html.H2('Average speed by year graph', style={'color': 'white'}),
            html.Div('Select year start to display the number of finishers:', style={'color': 'white'}),
            dcc.Input(id='start-year-input_avgspeed', type='number', value=1903, min=1903, max=2022),
            html.Div('Select year end to display the number of finishers:', style={'color': 'white'}),
            dcc.Input(id='end-year-input_avgspeed', type='number', value=2021, min=1903, max=2022),
            dcc.Graph(id='avgspeed-graph')
        ], style={'padding': '20px', 'animation': 'fade-in 1s'}),

    elif tab == 'tab-3':
        return html.Div([
            html.H2('Compare time of first riders for a year bar graph', style={'color': 'white'}),
            html.Div('Select year to display:', style={'color': 'white'}),
            dcc.Input(id='yearToDisplay-input', type='number', value=1903, min=1903, max=2022),
            html.Div('Select riders to display:', style={'color': 'white'}),
            dcc.Dropdown(
                id='timeOfFirsts-dropdown',
                options=[
                    {'label': 'First Rider', 'value': 'first_rider'},
                    {'label': 'Second Rider', 'value': 'second_rider'},
                    {'label': 'Third Rider', 'value': 'third_rider'}
                ],
                value=['first_rider', 'second_rider', 'third_rider'],
                multi=True,
                style={'color': 'black'}
            ),
            html.Div('Select time ladder:', style={'color': 'white'}),
            dcc.Dropdown(
                id='time_Ladder-dropdown',
                options=[
                    {'label': 'Hour', 'value': 'hour'},
                    {'label': 'Minute', 'value': 'minute'},
                    {'label': 'Second', 'value': 'second'}
                ],
                value='hour',
                multi=False,
                style={'color': 'black'}
            ),
            dcc.Graph(id='timeOfFirsts-graph')
        ], style={'padding': '20px', 'animation': 'fade-in 1s'}),

    elif tab == 'tab-4':
        return html.Div([
            html.H2('Compare time of first riders by year multiline graph', style={'color': 'white'}),
            html.Div('Select year start to display:', style={'color': 'white'}),
            dcc.Input(id='start_year-input', type='number', value=1903, min=1903, max=2022),
            html.Div('Select year end to display:', style={'color': 'white'}),
            dcc.Input(id='end_year-input', type='number', value=2021, min=1903, max=2022),
            html.Div('Select time ladder:', style={'color': 'white'}),
            dcc.Dropdown(
                id='timeLadder-dropdown',
                options=[
                    {'label': 'Hour', 'value': 'hour'},
                    {'label': 'Minute', 'value': 'minute'},
                    {'label': 'Second', 'value': 'second'}
                ],
                value='hour',
                multi=False,
                style={'color': 'black'}
            ),
            dcc.Graph(id='multilineFirsts-graph')
        ], style={'padding': '20px', 'animation': 'fade-in 1s'}),
    
    else:
        return html.Div([
            html.H3('Tab content 1')
        ], style={'padding': '20px', 'color': 'white', 'animation': 'fade-in 1s'})

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
    [Input('timeOfFirsts-dropdown', 'value'),
     Input('yearToDisplay-input', 'value'),
     Input('time_Ladder-dropdown', 'value')]
)
def update_timeOfFirsts_graph(selected_riders, yearToDisplay, time_ladder):
    firstRider = 'first_rider' in selected_riders
    secondRider = 'second_rider' in selected_riders
    thirdRider = 'third_rider' in selected_riders
    fig = graphTimeOfFirst(dfFinishers, yearToDisplay, firstRider, secondRider, thirdRider, time_ladder)
    return fig

@app.callback(
    Output('multilineFirsts-graph', 'figure'),
    [Input('start_year-input', 'value'),
     Input('end_year-input', 'value'),
     Input('timeLadder-dropdown', 'value')]
)
def update_multilineFirsts_graph(start_year, end_year, time_ladder):
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
    [Input('start-year-input2', 'value'),
     Input('end-year-input2', 'value')]
)
def update_average_between_starters_and_finishers(start_year, end_year):
    fig = graphTheAverageBetweenStartersAndFinishers(dfTours, start_year, end_year)
    return fig

# Ajout de styles et animations CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Data Visualisation Application</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: #1a1a1a;
                font-family: Arial, sans-serif;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }
            @keyframes fade-in {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div id="react-entry-point">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
