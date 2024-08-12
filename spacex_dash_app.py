# Import required libraries
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'}] +
                     [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                ),
    html.Br(),

    # TASK 2: Add a pie chart to show the proportion of successful launches by site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]
                   ),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Filter for successful launches across all sites
        successful_launches = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(successful_launches, names='Launch Site',
                     title='Successful Launches by Site Across All Sites')
    else:
        # Filter for successful launches at a specific site
        successful_launches = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['class'] == 1)]
        fig = px.pie(successful_launches, names='Launch Site',
                     title=f'Successful Launches by Site for {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Payload Mass vs. Launch Success')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8051)  # Use a different port if 8050 is in use
