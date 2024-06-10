from dash import html, dcc, Dash, callback, Input, Output
from DataTransformation import SalesCalulation
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

image_path = "assets/Graph_Image.png"

df = pd.read_csv("Final_data.csv")
df = df.sort_values(by="date")

full_df = pd.read_csv("combined_data_full.csv")
full_df = SalesCalulation(full_df)

product = list(full_df["product"].unique())
product.append("all")
# creating options for product
option = {}
for i in product:
    option[i] = i.upper()


regions = list(df["region"].unique())
regions.append("all")
regions = [i.capitalize() for i in regions]

colors = {
    "primary": "#303937",
    "secondary": "#9EA9B1",
    "font": "#522A61",
}


pie_chart_fig = px.pie(
    full_df, values="sales", names="product", labels={"product": "Product"}
)
pie_chart_fig.update_layout(
    plot_bgcolor=colors["secondary"],
    paper_bgcolor=colors["primary"],
    font_color="white",
)

app = Dash(__name__)


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "MORSEL SALES REPORT",
                    style={
                        "textAlign": "center",
                        "background-color": colors["secondary"],
                        "margin": "0",
                        "flex": "1",
                        "color": "black",
                    },
                    className="banner",
                ),
                html.Img(
                    src=app.get_asset_url("Graph_Image.png"),
                    style={
                        "margin": "0 10px 0 0",
                        "padding": "0",
                        "background-color": colors["secondary"],
                    },
                    className="banner-img",
                ),
            ],
            className="banner",
        ),
        html.Div(
            [
                html.H2(
                    "Pink Morsel Sales by Region",
                    style={
                        "textAlign": "center",
                        "background-color": colors["secondary"],
                    },
                ),
                dcc.RadioItems(
                    regions,
                    "Regions",
                    id="Region",
                    style={
                        "textAlign": "left",
                        "background-color": colors["secondary"],
                    },
                    inline=True,
                ),
            ],
            className="banner-radio",
        ),
        html.Div(
            [
                dcc.Graph(
                    id="pink-morsel-line",
                    figure={
                        "layout": go.Layout(
                            xaxis={"showgrid": False}, yaxis={"showgrid": False}
                        )
                    },
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Product Sales Distribution",
                                    style={
                                        "textAlign": "center",
                                        "background-color": colors["secondary"],
                                    },
                                ),
                                dcc.Dropdown(
                                    options=option,
                                    value="gold-morsel",
                                    id="product_dropdown",
                                ),
                                dcc.Graph(id="product-sales-pie", figure=pie_chart_fig),
                            ]
                        )
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [
                        html.H2(
                            "Sales Between Duration",
                            style={
                                "textAlign": "center",
                                "background-color": colors["secondary"],
                            },
                        ),
                        html.Div(
                            [
                                dcc.DatePickerRange(
                                    id="date-range",
                                    min_date_allowed=full_df["date"].min(),
                                    max_date_allowed=full_df["date"].max(),
                                    start_date=full_df["date"].min(),
                                    end_date=full_df["date"].max(),
                                    style={"size": "1px"},
                                ),
                            ]
                        ),
                        dcc.Graph(id="sales-between-dates"),
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                    },
                ),
            ],
            style={"width": "100%", "display": "inline-block", "align": "left"},
        ),
        # for sales trend graph
        # for sales trend graph
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Product Price Trend",
                            style={
                                "textAlign": "center",
                                "background-color": colors["secondary"],
                            },
                        ),
                        dcc.Graph(id="product_price_trend"),
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [
                        html.H2(
                            "Sales Summary B/w Duration",
                            style={
                                "textAlign": "center",
                                "background-color": colors["secondary"],
                            },
                        ),
                        html.Div(
                            [
                                html.Div(id="total-sales-tile", className="tile"),
                                html.Div(id="max-sales-day-tile", className="tile"),
                                html.Div(id="avg-sales-day-tile", className="tile"),
                                html.Div(id="avg-sales-growth-tile", className="tile"),
                            ],
                            className="number-tiles-grid",
                        ),
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
            ],
            style={"display": "flex"},
        ),
    ]
)


@callback(Output("pink-morsel-line", "figure"), Input("Region", "value"))
def update_graph(Region):

    if Region != "All":
        Region = Region.lower()
        Regional_data = df.loc[df["region"] == Region]
    else:
        Regional_data = df

    fig = px.line(
        Regional_data,
        x="date",
        y="sales",
        hover_data="sales",
        labels={"date": "Date", "sales": "Sales"},
    )
    fig.update_layout(
        plot_bgcolor=colors["secondary"],
        paper_bgcolor=colors["primary"],
        font_color=colors["font"],
    )
    fig.update_xaxes(color="white")
    fig.update_yaxes(color="white")
    # fig.update_traces(line_color='#25DAB0')
    return fig


@callback(
    Output("sales-between-dates", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("product_dropdown", "value"),
    ],
)
def update_sales_between_dates(start_date, end_date, product_dropdown):
    filtered_df = full_df[
        (full_df["date"] >= start_date)
        & (full_df["date"] <= end_date)
        & (full_df["product"] == product_dropdown)
    ]
    fig = px.line(
        filtered_df, x="date", y="sales", labels={"date": "Date", "sales": "Sales"}
    )
    fig.update_layout(
        plot_bgcolor=colors["secondary"],
        paper_bgcolor=colors["primary"],
        font_color="white",
    )
    return fig


@callback(Output("product_price_trend", "figure"), Input("product_dropdown", "value"))
def product_price_trend(product_dropdown):
    print(product_dropdown)
    if product_dropdown != "All":
        product_sales = full_df.loc[full_df["product"] == product_dropdown]
    fig = px.line(
        product_sales, x="date", y="price", labels={"date": "Date", "price": "Price"}
    )
    fig.update_layout(
        plot_bgcolor=colors["secondary"],
        paper_bgcolor=colors["primary"],
        font_color="white",
    )
    return fig


@callback(
    [
        Output("total-sales-tile", "children"),
        Output("max-sales-day-tile", "children"),
        Output("avg-sales-day-tile", "children"),
        Output("avg-sales-growth-tile", "children"),
    ],
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("product_dropdown", "value"),
    ],
)
def number_tiles(start_date, end_date, product_dropdown):
    filtered_data = full_df[
        (full_df["date"] >= start_date)
        & (full_df["date"] <= end_date)
        & (full_df["product"] == product_dropdown)
    ]
    total_sales = filtered_data["sales"].sum()
    max_sales_per_day = filtered_data["sales"].max()
    average_sales_per_day = filtered_data["sales"].mean()

    if len(filtered_data) > 1:
        end_sales_fig = filtered_data["sales"].iloc[-1]
        start_sales_fig = filtered_data["sales"].iloc[0]
        divisor = max(end_sales_fig, start_sales_fig)
        sales_growth = abs(end_sales_fig - start_sales_fig) * 100 / divisor
        print(sales_growth)

    else:
        sales_growth = 0

    print(filtered_data["sales"].iloc[-1], filtered_data["sales"].iloc[0])
    return (
        f"Total Sales: {total_sales:.2f}",
        f"Max Sales/Day: {max_sales_per_day:.2f}",
        f"Avg Sales/Day: {average_sales_per_day:.2f}",
        f"Sales Diff: {sales_growth:.2f}%",
    )


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})


if __name__ == "__main__":
    app.run(debug=True)
