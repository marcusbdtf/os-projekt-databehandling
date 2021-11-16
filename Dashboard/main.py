import pandas as pd
from dash import dcc, html
import dash
import plotly_express as px
from dash.dependencies import Input, Output
from process_data import get_italy_data
from process_data import process_data

italy_df = get_italy_data()
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Italy Olympics Graphs'),
    dcc.Dropdown(id='olympics-dropdown',
                    options=[{'label': i, 'value': i}
                    for i in italy_df.iloc[:,0:-1]], # excluding last column "Total", it's a useless graph
                    value='Sport'),
    dcc.Graph(id='medals-graph')
])

@app.callback(
    Output(component_id='medals-graph', component_property='figure'),
    Input(component_id='olympics-dropdown', component_property='value')
)

def update_graph(selected_option):
    filtered_italy = process_data(italy_df, selected_option)

    if selected_option == 'Age' or selected_option == 'Height' or selected_option == 'Weight':
        fig = px.scatter(filtered_italy, x=selected_option ,
                        y = 'Total', color='Total', 
                        title=f'Total number of medals / {selected_option}')

    elif selected_option == 'Sex' or selected_option == 'Season':
        fig = px.pie(filtered_italy, selected_option ,
                        'Total', color='Total', 
                        title=f'Total number of medals per /  {selected_option}')
    
    elif selected_option == 'Medal':
        fig = px.bar(process_data(italy_df, selected_option),
                    x = selected_option, y = "Total",
                    color = selected_option,
                    title=f'Total number of medals')
        
    else:     
        fig = px.bar(filtered_italy,
                    x = selected_option, y = 'Total',
                    color= selected_option,
                    title=f'Total number of medals / {selected_option}')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)