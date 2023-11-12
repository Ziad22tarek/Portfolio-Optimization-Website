import dash
from dash import html
from dash_app.create_main_div import create_main_div
from dash_app.create_result_div import create_result_div
from dash_app.create_callback import create_callback

app=dash.Dash(title='Portfolio Optimizer',
              meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],
              )



app.layout=html.Div([create_main_div(),create_result_div()])


create_callback(app)

app.run_server(threaded=True)
