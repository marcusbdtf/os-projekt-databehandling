import pandas as pd
from dash import dcc, html
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import hashlib as hl

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


fig = make_subplots(1,2)
fig.add_trace(
    go.Bar(
        x=italy_most_medals["Sport"], 
        y=italy_most_medals["Medal"]
        )
    )
fig.add_trace(
    go.Bar(
        x=italy_most_medals[0:10]["Sport"], 
        y=italy_most_medals[0:10]["Medal"]),
    row=1,col=2)


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Olympics Data"),
    
    dcc.Graph(id='os-graph', figure=fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)