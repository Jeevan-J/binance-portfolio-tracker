"""
This is a simple dashboard for the binance portfolio tracker application written using Plotly Dash.
"""

import os
import dateparser

from pages import spot
from database import BinanceDB, SQLITE
from functions import binance_get_all_orders_by_pair, get_date_from_unix_ms

from dash import Dash, html, dcc, Input, Output, State
from binance.client import Client

from dotenv import load_dotenv
load_dotenv()


# Database Initialization
binance_dbms = BinanceDB(SQLITE, dbname='data/binance.db')
binance_dbms.create_db_tables()

# App Initialization
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "Portfolio Tracker"
app._serve_default_favicon = app.get_asset_url("PortfolioTrackerLogos/favicon.ico")
server = app.server

# Binance Client
if os.getenv('ENVIRONMENT','TEST').upper() == 'PROD':
    binance_client = Client(
        os.getenv("BINANCE_PROD_API_KEY"), 
        os.getenv("BINANCE_PROD_API_SECRET_KEY")
    )
else:
    binance_client = Client(
        os.getenv("BINANCE_TEST_API_KEY"), 
        os.getenv("BINANCE_TEST_API_SECRET_KEY")
    )
    binance_client.API_URL = 'https://testnet.binance.vision/api'

# App Layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    """
    This is a callback function that updates the page content based on the pathname.

    Args:
        pathname (str): current page url pathname

    Returns:
        dash component: portfolio page
    """
    if pathname == '/':
        return spot.create_layout(app, binance_client, binance_dbms=binance_dbms)
    else:
        return html.Div([
            html.H1("404"),
            html.Hr(),
            html.P("The page you are looking for does not exist."),
        ])

@app.callback(Output('add-pair-out','children'), 
              Input('add-pair-submit','n_clicks'),
              [State('add-pair-name','value'), State('add-pair-startTime','value')],
              prevent_initial_callback=True)
def add_pair(n, pair_name, pair_start_time):
    """
    This is a simple callback function that adds a new pair to the database.

    Args:
        n (int): _description_
        pair_name (str): _description_
        pair_startTime (str): _description_

    Returns:
        list: _description_
    """
    if pair_start_time and pair_name:
        pair_start_time = dateparser.parse(pair_start_time)
        latest_time = binance_dbms.get_last_time_for_symbol(pair_name)
        print(pair_start_time, latest_time)
        if latest_time:
            pair_start_time = get_date_from_unix_ms(latest_time)
        orders_df = binance_get_all_orders_by_pair(binance_client, pair_name, pair_start_time)
        orders_df.rename(columns={'type':'orderType'}, inplace=True)
        orders_df.to_sql(
            "orders",
            binance_dbms.db_engine.connect(),
            if_exists="append",
            index=False)
        return ["Added "+pair_name+" !!"]
    else:
        return ["Provide both Pair and Start Date!"]

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=False)
    # app.run_server(debug=True)
    