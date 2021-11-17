from os import path
import pandas as pd
from dash import dcc, html
import dash
import plotly_express as px
from dash.dependencies import Input, Output
from process_data import get_all_countries
from process_data import get_italy_data
from process_data import process_data
import dash_bootstrap_components as dbc

italy_df = get_italy_data()
all_countries_df = get_all_countries()
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
                             for i in italy_df.columns if i != "Total"],
                    value='Sport',
                    style={
                        "width": "50%",
                    },
                 ),
    dcc.Graph(id='medals-graph',
              figure={},
              style={
                  'height': 500,
                  'width': 900,
              },
              ),
], style={'margin': 'auto', 'width': "50%"},
    # style = {"display": "flex"}
)

@app.callback(
    Output(component_id='medals-graph', component_property='figure'),
    [Input("url", "pathname")],
    Input(component_id='olympics-dropdown', component_property='value'),
)

def update_graph(pathname, selected_option):
    fig=0
    
    if pathname == "/":
        filtered_df = italy_df
    else:
        filtered_df = all_countries_df

    if selected_option == 'Age' or selected_option == 'Height' or selected_option == 'Weight':
        fig = px.scatter(process_data(filtered_df, selected_option), selected_option,
                         'Total',
                         color='Total',
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

# @ app.callback(
#     dash.dependencies.Output("page-content", "children"),
#     [Input("url", "pathname")]
# )

# def load_my_page(pathname):
#     fig=""
#     if pathname == "/":
#         fig = update_graph(pathname, italy_df)

#     elif pathname == "/page-2":
#         fig = update_graph(pathname, all_countries_df)
#     return {"data": [fig]}


if __name__ == '__main__':
    app.run_server(debug=True)
