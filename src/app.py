import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the weather data CSV
df = pd.read_csv('data/tanzania_zanzibar_cities_weather_data.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H2("Weather Dashboard for Cities in Tanzania"),
    
    # Dropdown for selecting city
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in df['City'].unique()],
        value='Dar es Salaam',
        style={'width': '50%'}
    ),
    
     # Graphs arranged in a 2-column layout
    html.Div([
        html.Div([dcc.Graph(id='sunshine-graph')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='rain-graph')], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    
    html.Div([
        html.Div([dcc.Graph(id='precipitation-graph')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='water-temp-graph')], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    
    html.Div([
        html.Div([dcc.Graph(id='humidity-rel-graph')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='humidity-abs-graph')], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'})
])

# Callback for updating graphs based on city selection
@app.callback(
    [Output('sunshine-graph', 'figure'),
     Output('rain-graph', 'figure'),
     Output('precipitation-graph', 'figure'),
     Output('water-temp-graph', 'figure'),
     Output('humidity-rel-graph', 'figure'),
     Output('humidity-abs-graph', 'figure')],
    [Input('city-dropdown', 'value')]
)
def update_graphs(selected_city):
    filtered_df = df[df['City'] == selected_city]

    # Hours of sunshine
    sunshine_fig = px.bar(
        filtered_df, x='Month', y='Hours of sunshine per day', 
        title=f'Hours of Sunshine per Day - {selected_city}', 
        labels={'Hours of sunshine per day': 'Hours'}
    )

    # Rain days per month
    rain_fig = px.bar(
        filtered_df, x='Month', y='Rain days per month', 
        title=f'Rain Days per Month - {selected_city}', 
        labels={'Rain days per month': 'Days'}
    )

    # Precipitation
    precipitation_fig = px.bar(
        filtered_df, x='Month', y='Precipitation in mm/day', 
        title=f'Precipitation in mm/day - {selected_city}', 
        labels={'Precipitation in mm/day': 'mm'}
    )

    # Water temperature
    water_temp_fig = px.bar(
        filtered_df, x='Month', y='Water temperature (°C)', 
        title=f'Water Temperature (°C) - {selected_city}', 
        labels={'Water temperature (°C)': '°C'}
    )

    # Relative humidity
    humidity_rel_fig = px.bar(
        filtered_df, x='Month', y='Relative humidity (%)', 
        title=f'Relative Humidity (%) - {selected_city}', 
        labels={'Relative humidity (%)': '%'}
    )

    # Absolute humidity
    humidity_abs_fig = px.bar(
        filtered_df, x='Month', y='Absolute humidity in g/m³', 
        title=f'Absolute Humidity in g/m³ - {selected_city}', 
        labels={'Absolute humidity in g/m³': 'g/m³'}
    )

    return sunshine_fig, rain_fig, precipitation_fig, water_temp_fig, humidity_rel_fig, humidity_abs_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
