import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from data import getDatasFromTDFFinishers, getDatasFromTDFStages, getDatasFromTDFTours
from data import graphNumberOfFinisher, graphAverageSpeed, graphTimeOfFirst

# Créer une instance de l'application Dash
app = dash.Dash(__name__)

# Charger et préparer les données
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

dfFinishers = getDatasFromTDFFinishers()
dfStages = getDatasFromTDFStages()
dfTours = getDatasFromTDFTours()
startYear = 1903
endYear = 2022
compareStarters = False

# Définir la disposition de l'application
app.layout = html.Div(children=[
    html.H1(children='Data Visualisation Application'),

    html.Div(children='''
        Select fruits to display:
    '''),

    dcc.Dropdown(
        id='fruit-dropdown',
        options=[
            {'label': 'Apples', 'value': 'Apples'},
            {'label': 'Oranges', 'value': 'Oranges'},
            {'label': 'Bananas', 'value': 'Bananas'}
        ],
        value=['Apples', 'Oranges', 'Bananas'],
        multi=True
    ),

    dcc.Graph(
        id='example-graph'
    ),
    
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
        value=[],  # Default value
        labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Graph(
        id='finisher-graph'
    )
])

# Définir les callbacks pour mettre à jour le graphique en fonction de la sélection du dropdown
@app.callback(
    Output('example-graph', 'figure'),
    Input('fruit-dropdown', 'value')
)
def update_graph(selected_fruits):
    filtered_df = df[df['Fruit'].isin(selected_fruits)]
    fig = px.bar(filtered_df, x="Fruit", y="Amount", color="City", barmode="group")
    return fig


@app.callback(
    Output('finisher-graph', 'figure'),
    [Input('start-year-input', 'value'),
     Input('end-year-input', 'value'),
     Input('show-finishers-checklist', 'value')]
)
def update_finisher_graph(start_year, end_year, show_finishers_checklist):
    show_finishers = 'show_starters' in show_finishers_checklist
    print(f"show_finishers: {show_finishers}")
    fig = graphNumberOfFinisher(dfTours, start_year, end_year, show_finishers)
    return fig


# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
