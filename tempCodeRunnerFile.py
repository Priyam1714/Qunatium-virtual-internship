from dash import html,dcc, Dash
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('Final_data.csv')
df.sort_values(by='date')


fig = px.line(df,x='date',y='sales')

regions = list(df['region'].unique())
print(regions)
regions.append('all')
regions = [i.capitalize() for i in regions]
print(regions)