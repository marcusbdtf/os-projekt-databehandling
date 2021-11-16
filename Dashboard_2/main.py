import pandas as pd
from dash import dcc, html
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import hashlib as hl
import plotly_express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
pd.options.plotting.backend = "plotly"

"""Data"""
athletes = pd.read_csv("Data/athlete_events.csv")
hashed_names = athletes["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
athletes.insert(1,"Hashed name", hashed_names)
athletes = athletes.drop(columns="Name")

italy_df = athletes.drop_duplicates(subset=["Medal", "Games","Event"])
italy_df = italy_df[italy_df["NOC"]=="ITA"]
italy_most_medals = italy_df.groupby("Sport").count().reset_index()
italy_most_medals = italy_most_medals.sort_values(by="Medal",ascending=False)

def process_data(old_df, col):
    filtered_df = old_df.groupby(col).count().reset_index()
    filtered_df = filtered_df.sort_values(by=col, ascending=False)
    return filtered_df 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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


sidebar = html.Div([
    html.H2("Sidebar", className="display-4"),
    html.Hr(),
    html.P(
        "Historic olympic performances"
    ),
        dbc.Nav([
         dbc.NavLink("Italy Statistics", href="/", active="exact"),
            dbc.NavLink("Sports statistics", href="/page-2", active="exact"),
          ],
          vertical=True,
          pills=True,
        ),
    ],
    style=sidebar_layout,
)

content = html.Div(id="page-content", children=[], style=content_layout)

app.layout = html.Div([
    sidebar,
    content,
    dcc.Location(id="url"),
    html.H1('Italy Olympics Graphs'),
    dcc.Dropdown(id='olympics-dropdown',
                    options=[{'label': i, 'value': i}
                    for i in italy_df],
                    value='Sport',
                    style={
                            "width": "50%",
                        },
                    ),
    dcc.Graph(id='medals-graph',
              style={
                    'height': 500,
                    'width': 900,
                    },
                ),
    ], style = {'margin':'auto','width': "50%"}
    #style = {"display": "flex"}
)

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    Input(component_id='olympics-dropdown', component_property='value')
    
    
)
def page_loader(pathname, selected_option):
    if pathname == "/":
        return update_graph(selected_option)

    elif pathname == "page-2":
        pass

@app.callback(
    Output(component_id='medals-graph', component_property='figure'),
    Input(component_id='olympics-dropdown', component_property='value'),
)
def update_graph(selected_option):
    filtered_italy = process_data(italy_df, selected_option)

    if selected_option == 'Age' or selected_option == 'Height' or selected_option == 'Weight':
        fig = px.scatter(filtered_italy, x=selected_option ,
                        y = 'Medal', color='Medal', 
                        title=f'Gold Medals in {selected_option}')

    elif selected_option == 'Sex' or selected_option == 'Season':
        fig = px.pie(filtered_italy, selected_option ,
                        'Medal', color='Medal', 
                        title=f'Gold Medals divided by {selected_option}')
    
    elif selected_option == 'Medal':
        fig = px.bar(process_data(italy_df, selected_option).sort_values(by="ID", ascending=False),
                    x = selected_option, y = "ID",
                    color = selected_option,
                    title=f'Medal distribution')
        
    else:     
        fig = px.bar(filtered_italy,
                    x = selected_option, y = 'Medal',
                    color= selected_option,
                    title=f'Gold Medals in {selected_option}')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)