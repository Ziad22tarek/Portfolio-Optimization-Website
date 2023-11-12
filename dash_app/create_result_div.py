import dash_table
from dash import html,dcc
from dash_app.convert_image_to_data_uri import convert_image_to_data_uri



def create_result_div():
    """
    Generates the result division of the Dash application, containing summary and statistics pages.

    Returns:
    result_div (dash.html.Div): Result division containing summary and statistics pages.

    """

    # Define styles for the result div and individual pages
    result_div_style = {
        'width': '70%',
        'background-color': '#1C1C1C',
        'position': 'absolute',
        'top': '0',
        'right': '0',
        'margin-left': '28%',
    }

    page_style = {
        'width': '95%',
        'background-color': 'white',
        "box-shadow": "3px 3px 20px rgba(100, 100, 100, 100)",
        'margin': '3%',
        'margin-top': '1%'
    }

    # Define content for summary_stock_page
    summary_stock_page = html.Div(
        style=page_style,
        children=[
            html.H1('Summary of portfolio stocks', style={'margin-left': '2%', 'font-weight': 'bold', 'height': '10vh'}),
            dcc.Graph(id='Adj Close Figure Plot', figure={}, style={'width': '100%', 'height': '700px', 'margin-bottom': '2%'}),
            dcc.Graph(id='Correlation Figure', figure={})
        ])

    # Define content for portfolio_statistics_page
    portfolio_statistics_page = html.Div(
        style=page_style,
        children=[
           # html.Img(src=convert_image_to_data_uri('Discover Data Log .jpg'),style={'width':'5%','height':'5vh'}),
            html.H1('Portfolio Statistics', style={'margin-left': '2%', 'font-weight': 'bold', 'height': '10vh'}),
            html.H3('Optimal Portfolios:', style={'margin-left': '2%'}),
            html.Div(style={'width': '80%', 'height': '20vh', 'margin-left': '2%'}, children=[
                dash_table.DataTable(id='table-container', page_action='none',)
            ]),
            dcc.Graph(id='efficient frontier figure', figure={}),
            dcc.Graph(id='Individual Stocks figure', figure={})
        ])

    # Combine the pages into the result_div
    result_div = html.Div(style=result_div_style, children=[summary_stock_page, portfolio_statistics_page])

    return result_div
