import pandas as pd
from dash import dcc, html
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import hashlib as hl
import plotly_express as px
from dash.dependencies import Input, Output
pd.options.plotting.backend = "plotly"

"""Data"""
athletes = pd.read_csv("Data/athlete_events.csv")
hashed_names = athletes["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
athletes.insert(1,"Hashed name", hashed_names)
athletes = athletes.drop(columns="Name")

italy_df = athletes.drop_duplicates(subset=["Medal", "Games","Event"])
italy_df = italy_df[italy_df["Team"]=="Italy"]
italy_most_medals = italy_df.groupby("Sport").count().reset_index()
italy_most_medals = italy_most_medals.sort_values(by="Medal",ascending=False)

def process_data(old_df, col):
    filtered_df = old_df.groupby(col).count().reset_index()
    filtered_df = filtered_df.sort_values(by=col, ascending=False)
    return filtered_df 

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Italy Olympics Graphs'),
    dcc.Dropdown(id='olympics-dropdown',
                    options=[{'label': i, 'value': i}
                    for i in italy_df],
                    value='Sport'),
    dcc.Graph(id='medals-graph')
])

@app.callback(
    Output(component_id='medals-graph', component_property='figure'),
    Input(component_id='olympics-dropdown', component_property='value')
)

def update_graph(selected_option):
    filtered_italy = process_data(italy_df, selected_option)
    fig = px.bar(filtered_italy,
                    x = selected_option, y = 'Medal',
                    color='Sport',
                    title=f'Gold Medals in {selected_option}')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)