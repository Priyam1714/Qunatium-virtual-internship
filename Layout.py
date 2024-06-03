from dash import html,dcc, Dash
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('Final_data.csv')
df.sort_values(by='date')


fig = px.line(df,x='date',y='sales')
app.layout = html.Div( children= [
    html.H1('Pink Morsel Sales Vs Price Graph',style={'textAlign':'center','color':'black'}),
    dcc.Graph(
        id = 'pink-morsel-line',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)