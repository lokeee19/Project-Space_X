#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install plotly dash')
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# In[4]:


# Replace 'data' with the variable that contains the data you provided
data = "spacex_launch_dash.csv"

# Use StringIO to convert the multi-line string to a pandas DataFrame
df = pd.read_csv(data)
df


# In[41]:


import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Assume that you already loaded the data into the 'df' DataFrame

# Initialize the Dash app
app = dash.Dash(__name__)

# Calculate the minimum and maximum payload values
min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()

# Create the layout of the dashboard
app.layout = html.Div([
    html.H1('SpaceX Dashboard', style={'text-align': 'left', 'margin-left': '10px'}),  # Left-aligned main heading
    
    # Dropdown widget for selecting specific launch sites
    dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'All'}]
                 + [{'label': site, 'value': site} for site in df['Launch Site'].unique()],
                 value='All', placeholder='Select a Launch Site', style={'width': '50%', 'margin-left': '10px'}),
    
    # Range Slider to select payload range
    html.Div([
        html.Label('Payload Mass (kg)', style={'margin-top': '10px', 'margin-left': '10px'}),
        dcc.RangeSlider(
            id='payload-slider',
            min=min_payload,
            max=max_payload,
            value=[min_payload, max_payload],
            marks={min_payload: str(min_payload), max_payload: str(max_payload)},
            step=1000,
            pushable=500,  # Allows the user to select values in between the step intervals
            tooltip={'placement': 'bottom'}
        ),
    ]),
    
    # Pie chart to display the launch site proportions or success/failure proportions
    html.Div([
        dcc.Graph(id='site-pie-chart')
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '20px'}),
    
    # Scatter plot to display payload mass vs. launch success
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '20px'})
])

# Define a function to calculate the proportion of each launch site
def calculate_site_proportions(site_name, min_payload, max_payload):
    if site_name == 'All':
        filtered_df = df[(df['Payload Mass (kg)'] >= min_payload) & (df['Payload Mass (kg)'] <= max_payload)]
        site_proportions_df = filtered_df['Launch Site'].value_counts(normalize=True)
    else:
        filtered_df = df[(df['Payload Mass (kg)'] >= min_payload) & (df['Payload Mass (kg)'] <= max_payload) & (df['Launch Site'] == site_name)]
        site_proportions_df = filtered_df['class'].value_counts(normalize=True)
    
    return site_proportions_df

# Define the callback function to update the pie chart and scatter plot based on dropdown selection and payload range
@app.callback(
    [Output('site-pie-chart', 'figure'),
     Output('success-payload-scatter-chart', 'figure')],
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_charts(entered_site, payload_range):
    min_payload, max_payload = payload_range
    if entered_site == 'All':
        site_proportions_df = calculate_site_proportions('All', min_payload, max_payload)
        title_pie = 'Proportion of Launch Sites'
        colors_pie = ['lightblue', 'yellow', 'red', 'green']
        labels_pie = ['CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']  # Labels for pie chart legend
        fig_pie = px.pie(site_proportions_df, names=site_proportions_df.index, values=site_proportions_df.values, 
                         title=title_pie, color_discrete_sequence=colors_pie, labels=labels_pie)
        
        filtered_df = df[(df['Payload Mass (kg)'] >= min_payload) & (df['Payload Mass (kg)'] <= max_payload)]
        title_scatter = 'Payload Mass vs. Launch Success for All Sites'
        fig_scatter = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Launch Site',
                                 color_discrete_map={'CCAFS LC-40': 'lightblue', 'VAFB SLC-4E': 'yellow', 
                                                     'KSC LC-39A': 'red', 'CCAFS SLC-40': 'green'},
                                 title=title_scatter, labels={'class': 'Launch Success', 'Payload Mass (kg)': 'Payload Mass (kg)'})
        
    else:
        site_proportions_df = calculate_site_proportions(entered_site, min_payload, max_payload)
        title_pie = f'Success and Failure Proportions for {entered_site}'
        colors_pie = ['yellow', 'lightblue']
        labels_pie = ['Failure', 'Success']  # Labels for pie chart legend
        fig_pie = px.pie(site_proportions_df, names=site_proportions_df.index, values=site_proportions_df.values, 
                         title=title_pie, color_discrete_sequence=colors_pie, labels=labels_pie)
        
        filtered_df = df[(df['Payload Mass (kg)'] >= min_payload) & (df['Payload Mass (kg)'] <= max_payload) & (df['Launch Site'] == entered_site)]
        title_scatter = f'Payload Mass vs. Launch Success for {entered_site}'
        fig_scatter = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Launch Site',
                                 color_discrete_map={'Failure': 'yellow', 'Success': 'lightblue'},
                                 title=title_scatter, labels={'class': 'Launch Success', 'Payload Mass (kg)': 'Payload Mass (kg)'})
    
    return fig_pie, fig_scatter

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:





# In[ ]:




