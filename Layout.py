from dash import html,dcc, Dash, callback, Input, Output
from DataTransformation import SalesCalulation
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

image_path = "assets/Graph_Image.png"

df = pd.read_csv('Final_data.csv')
df = df.sort_values(by='date')

full_df =pd.read_csv('combined_data_full.csv')
full_df =SalesCalulation(full_df)

product = list(full_df['product'].unique())
product.append('all')
#creating options for product
option = {}
for i in product:
    option[i]=i.upper()


regions = list(df['region'].unique())
regions.append('all')
regions = [i.capitalize() for i in regions]

colors = {
    "primary":"#303937",
    "secondary":"#9EA9B1",
    "font":"#522A61",
}


pie_chart_fig = px.pie(full_df, values='sales', names='product', labels={'product': 'Product'})
pie_chart_fig.update_layout(
    plot_bgcolor=colors["secondary"],
    paper_bgcolor=colors["primary"],
    font_color='white',
)

app = Dash(__name__)


app.layout = html.Div([  
    html.Div([     
        html.H1('Pink Morsel Sales Graph',style={'textAlign':'center',
                                                 "background-color":colors["secondary"],
                                                 'margin':'0',
                                                 'flex':'1',
                                                 "color":"black"},
                                                 className="banner",
                                                 ),
        html.Img(src=app.get_asset_url('Graph_Image.png'),style={
                                                'margin':'0 10px 0 0',
                                                "padding":'0',
                                                'background-color':colors['secondary'],
                                                 },className="banner-img")                                                        
            ],className="banner"),

    html.Div([
        dcc.RadioItems(regions,
                     'Regions',
                     id='Region',style={'textAlign':'left',
                                        "background-color":colors["secondary"]}
                                        ,inline=True)
                                     
    ],className="banner-radio"),

    html.Div([
        dcc.Graph(id = 'pink-morsel-line',
              figure={
                "layout":go.Layout(
                    xaxis={'showgrid' : False },
                    yaxis={'showgrid' : False }
                    )}
                    )
    ]),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H2("Product Sales Distribution",style={'textAlign':'center','background-color':colors["secondary"]}),
                    dcc.Dropdown(options=option,value='gold-morsel',id='product_dropdown'),
                    dcc.Graph(id='product-sales-pie',figure=pie_chart_fig)
                ])
            ], style={'width': '50%', 'display': 'inline-block','vertical-align':'top'}),

            html.Div([
                    html.H2("Sales Between Duration",style={'textAlign':'center','background-color':colors["secondary"]}),
                    dcc.DatePickerRange(id='date-range',
                                        min_date_allowed=full_df['date'].min(),
                                        max_date_allowed=full_df['date'].max(),
                                        start_date=full_df['date'].min(),
                                        end_date=full_df['date'].max(),
                                        style={'font-size': '9px'}),
                    dcc.Graph(id='sales-between-dates')
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ],style={'width': '100%', 'display': 'inline-block','align':'left'}),

# for sales trend graph
        html.Div([
            html.Div([
                html.H2("Product Price Trend",style={'textAlign':'center','background-color':colors["secondary"]}),
                dcc.Graph(id='product_price_trend')
            ],style={'width': '50%', 'display': 'inline-block','vertical-align':'top'})
            ])

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
        plot_bgcolor=colors["secondary"],
        paper_bgcolor=colors["primary"],
        font_color=colors["font"],
         )
    fig.update_xaxes(color='white')
    fig.update_yaxes(color="white")
    #fig.update_traces(line_color='#25DAB0')
    return fig


@callback(
    Output('sales-between-dates','figure'),
    [Input('date-range','start_date'),
     Input('date-range','end_date')]
)
def update_sales_between_dates(start_date,end_date):
     filtered_df = full_df[(full_df['date'] >= start_date) & (full_df['date'] <= end_date)]
     fig = px.line(filtered_df,x='date',y='sales',labels={'date':'Date','sales':'Sales'})
     fig.update_layout(
     plot_bgcolor=colors["secondary"],
     paper_bgcolor=colors["primary"],
     font_color='white')
     return fig


@callback(
    Output('product_price_trend','figure'),
    Input('product_dropdown','value')
)
def product_price_trend(product_dropdown):
    print(product_dropdown)
    if product_dropdown != 'All':
        product_sales = full_df.loc[full_df['product']==product_dropdown]
    fig = px.line(product_sales,x='date',y='price',labels={'date':'Date','price':'Price'})
    fig.update_layout(
    plot_bgcolor=colors["secondary"],
    paper_bgcolor=colors["primary"],
    font_color=colors["white"],
     )
    return fig


app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run(debug=True) 
