from dash import html, dcc
import pandas as pd
import datetime

def create_main_div():
    """
    Generates the main user interface (UI) component of the Dash application.

    Returns:
    main_div (dash.html.Div): Main UI component containing various elements.

    """

    # Read the DataFrame from Excel
    df = pd.read_excel(r'.\S&P500 Company Ticker.xlsx')
    symbols_list = df['Ticker'].to_list()

    # Define styles for main_div and button
    main_div_style = {
        'width': '30%',
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'background-color': 'black',
        'height': '100vh'
    }

    button_style = {
        'backgroundColor': 'gray',
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'text-align': 'center',
        'text-decoration': 'none',
        'display': 'inline-block',
        'font-size': '16px',
        'border-radius': '5px',
        'cursor': 'pointer',
        'margin-top': '10vh',
        'margin-left': '10vh',
        'width': '20vh'
    }

    # Create DatePickerRange component
    date_picker_range = dcc.DatePickerRange(id='Date Picker',
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        min_date_allowed=datetime.date(2020, 1, 1),
        max_date_allowed=datetime.date.today(),
        style={'width': '98%'}
    )

    # Create main content Div
    content_div = html.Div(
        style={
            'backgroundColor': 'black',
            'width': '67%',
            'margin-left': '10vh',
            'height': '100vh'
        },
        children=[
            html.H1('Portfolio Optimizer', style={'color': 'white', 'font-weight': 'bold', 'font-size': '4.5vh'}),
            html.H3('Select Historical Time Periods (MM/DD/YYYY)', style={'color': 'white', 'margin-top': '20vh', 'font-size': '2.5vh'}),
            html.Div(children=[date_picker_range]),
            html.H3('Choose a portfolio of stocks', style={'color': 'white', 'margin-top': '6vh', 'font-size': '3vh'}),
            dcc.Dropdown(id='Stocks Dropdown',options=[{'label': symbol, 'value': symbol} for symbol in symbols_list], style={'width': '98%'}, placeholder='Select from S&P500 stocks!',multi=True),
            html.Button('Calculate!', id='Calculate Button',n_clicks=0, style=button_style)
        ]
    )

    # Create main Div
    main_div = html.Div(style=main_div_style, children=[content_div])

    
    
    
    
    
    
    
    
    return main_div
