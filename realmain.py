from os import path
import pandas as pd
from dash import dcc, html
import dash
from plotly.offline.offline import iplot
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
from process_data import get_all_countries
from process_data import get_italy_data
from process_data import process_data
from process_data import process_countries
from process_data import get_all_sports
import dash_bootstrap_components as dbc

italy_df = get_italy_data()
all_countries_df = get_all_countries()
sports_df = get_all_sports()
"""using our premade functions to get desired dataframes"""

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


content_layout = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar_layout = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "4rem 1rem 2rem",
    "background-color": "#f8f9fa",
} 
"""basic content & sidebar layout"""

sidebar = html.Div([
    html.Hr(),
    html.P(
        "Historic Olympic Performances"
    ),
    dbc.Nav([
            dbc.NavLink("Italy statistics", href="/", active="exact"),
            dbc.NavLink("Sports statistics", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
            ),
        ],style=sidebar_layout,
)
""" adding the desired elements to our sidebar """

content = html.Div(id="page-content", children=[], style=content_layout)

app.layout = html.Div([
    sidebar,
    content,
    dcc.Location(id="url"),
    html.H1('Various Olympic Graphs'),
    dcc.Dropdown(id='olympics-dropdown',
                    options=[{'label': i, 'value': i}
                             for i in italy_df.columns[1:] if i != "Total"],
                    value='Age',
                    style={
                        "width": "50%",
                    },
                 ),
    dcc.Graph(id='medals-graph',
              figure={},
              style={
                  'height': 700,
                  'width': 900,
              },
              ),
], style={'margin': 'auto', 'width': "50%"},)


"""
Setting up callbacks for our update graph function where we want to return a figure to dcc.Graph, depending on
#which sidebar tab is selected and what value in the dcc.Dropdown is selected.
# """
@app.callback(
    Output(component_id='medals-graph', component_property='figure'),
    [Input("url", "pathname")],
    Input(component_id='olympics-dropdown', component_property='value'),)

def update_graph(pathname, selected_option):
    """
    Function used to update graph depending on selected dropdown catergory
        Returns figure into "medals-graph - figure"
    """
    fig=0
    if pathname == "/": # checking what sidebar navigation we are on by using the "href"
        filtered_df = italy_df # because we know which sidebar tab we are on we can determine which dataframe we want to use

        if selected_option == 'Age' or selected_option == 'Height' or selected_option == 'Weight': 
            """Checking which dropdown element has been selected and then plotting accordingly """

            # using function "process_data" to get the desired dataframe structure

            fig = px.scatter(process_data(filtered_df, selected_option), selected_option, 
                         'Total',
                         color='Total', size='Total',
                         title=f'Total number of medals / {selected_option}')

        elif selected_option == 'Sex' or selected_option == 'Season':
            fig = px.pie(process_data(filtered_df, selected_option), selected_option,
                     'Total', color='Total',
                     title=f'Total number of medals per /  {selected_option}')

        elif selected_option == 'Medal':
            fig = px.bar(process_data(filtered_df, selected_option),
                     selected_option, "Total",
                     color=selected_option,
                     title=f'Total number of medals')

        else:
            fig = px.bar(process_data(filtered_df, selected_option),
                     selected_option, 'Total',
                     color=selected_option,
                     title=f'Total number of medals / {selected_option}')
        return fig
    else: 
        """Since we are only using two tabs we only have to identify one 'href' """
        filtered_df = sports_df # using desired dataframe for plotting

        if selected_option == 'Age': # not using "process data" since it's counter intuitive in this scenario
            football = sports_df[sports_df['Sport'] == 'Football']['Age'].dropna()
            Basketball = sports_df[sports_df['Sport'] == 'Basketball']['Age'].dropna()
            Bobsleigh = sports_df[sports_df['Sport'] == 'Bobsleigh']['Age'].dropna()
            Weightlifting = sports_df[sports_df['Sport'] == 'Weightlifting']['Age'].dropna() 
            sportsdata = [football, Basketball, Bobsleigh, Weightlifting]
            grouplabels = ['Football', 'Basketball', 'Bobsleigh', 'Weightlifting']
            """ here we are cleaning the data and adding it to variables and then into lists for easier use ff plotting """
            
            fig = ff.create_distplot(sportsdata, grouplabels, show_hist=False, show_rug=False)
            fig['layout'].update(title='Age distribution per sport')
            fig.update_layout(hovermode="x")
            fig.update_xaxes(
                showspikes = True, 
                spikedash = "solid",
                spikemode = "across",
                 spikecolor ="black",
                spikesnap = "cursor",
                )      
        
        elif selected_option == 'Height':
            fig = px.scatter(filtered_df, "Weight",
                     "Height",
                     color='Sport',
                     title=f'Height & weight between the different teams.')
            fig.update_layout(hovermode="x")
            fig.update_xaxes(
                showspikes = True, 
                spikedash = "solid",
                spikemode = "across",
                 spikecolor ="yellow",
                spikesnap = "cursor",
                )   

        elif selected_option == "Weight":
            football = sports_df[sports_df['Sport'] == 'Football']['Weight'].dropna()
            Basketball = sports_df[sports_df['Sport'] == 'Basketball']['Weight'].dropna()
            Bobsleigh = sports_df[sports_df['Sport'] == 'Bobsleigh']['Weight'].dropna()
            Weightlifting = sports_df[sports_df['Sport'] == 'Weightlifting']['Weight'].dropna()
        
            sportsdata = [football, Basketball, Bobsleigh, Weightlifting]
            grouplabels = ['Football', 'Basketball', 'Bobsleigh', 'Weightlifting']
            fig = ff.create_distplot(sportsdata, grouplabels, show_hist=False, show_rug=False,)
            fig['layout'].update(title='Weight distribution per sport')
            fig.update_layout(hovermode="x")
            fig.update_xaxes(
                showspikes = True, 
                spikedash = "solid",
                spikemode = "across",
                 spikecolor ="black",
                spikesnap = "cursor",)   

        elif selected_option == 'Medal':
            filtered_df = filtered_df.groupby(['NOC', 'Sport'])['Medal'].count().nlargest(50).reset_index()
            fig = px.scatter(filtered_df, "Sport",
                     "Medal",
                     color='NOC', size='Medal', symbol='NOC',
                     title=f'Total number of medals per sport & country. (Barplot)')

        else:
            filtered_df = filtered_df.groupby(['NOC', 'Sport'])['Medal'].count().nlargest(50).reset_index()
            fig = px.histogram(filtered_df, selected_option,
                     'Medal',
                     color="NOC",
                     title=f'Total number of medals per sport & country. (Scatterplot)')
        return fig # returns the figure based on which sidebar tab and then which element in the dropdown menu

if __name__ == '__main__':
    app.run_server(debug=True)
