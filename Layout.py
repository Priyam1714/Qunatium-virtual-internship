from dash import html,dcc, Dash, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('Final_data.csv')
df.sort_values(by='date')


regions = list(df['region'].unique())
regions.append('all')
regions = [i.capitalize() for i in regions]



app.layout = html.Div([  
    html.Div([     
        html.H1('Pink Morsel Sales Vs Price Graph',style={'textAlign':'center','color':'black'}),
        dcc.RadioItems(regions,
                     'Regions',
                     id='Region',style={'textAlign':'left'},inline=True)
    ]),
    dcc.Graph(id = 'pink-morsel-line',
              figure={
                "layout":go.Layout(
                    xaxis={'showgrid' : False },
                    yaxis={'showgrid' : False }
                    )}
                    )    
])

@callback(
    Output('pink-morsel-line','figure'),
    Input('Region','value')
)
def update_graph(Region):
    
    if Region !='All':
       Region = Region.lower()
       Regional_data = df.loc[df['region']==Region]
    else:
        Regional_data = df
    fig = px.line(Regional_data,x='date',y='sales',hover_data='sales',labels={'date':'Date','sales':'Sales'})
    fig.update_layout(
        plot_bgcolor='#000000')
    fig.update_traces(line_color='#6DBD13')
    return fig


if __name__ == '__main__':
    app.run(debug=True) 