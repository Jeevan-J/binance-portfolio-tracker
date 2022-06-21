from importlib.resources import path
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from binance.client import Client

import os
import dateparser
from dotenv import load_dotenv
load_dotenv()

from pages import (
    spot
)
from database import BinanceDB, SQLITE
from functions import binance_get_all_orders_by_pair, get_date_from_unix_ms

# Database Initialization
binance_dbms = BinanceDB(SQLITE, dbname='data/binance.db')
binance_dbms.create_db_tables()

# App Initialization
app = Dash(
    __name__,
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "Portfolio Tracker"
app._serve_default_favicon = app.get_asset_url("PortfolioTrackerLogos/favicon.ico")
server = app.server
# app.config.suppress_callback_exceptions = True

# Binance Client
if os.getenv('ENVIRONMENT','TEST').upper() == 'PROD':
    binance_client = Client(os.getenv("BINANCE_PROD_API_KEY"), os.getenv("BINANCE_PROD_API_SECRET_KEY"))
else:
    binance_client = Client(os.getenv("BINANCE_TEST_API_KEY"), os.getenv("BINANCE_TEST_API_SECRET_KEY"))
    binance_client.API_URL = 'https://testnet.binance.vision/api'

# App Layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    return spot.create_layout(app, binance_client, binance_dbms=binance_dbms)

@app.callback(Output('add-pair-out','children'), 
              Input('add-pair-submit','n_clicks'),
              [State('add-pair-name','value'), State('add-pair-startTime','value')],
              prevent_initial_callback=True)
def add_pair(n, pair_name, pair_startTime):
    print(pair_name)
    print(pair_startTime)
    if pair_startTime and pair_name:
        pair_startTime = dateparser.parse(pair_startTime)
        latest_time = binance_dbms.get_last_time_for_symbol(pair_name)
        print(pair_startTime, latest_time)
        if latest_time:
            pair_startTime = get_date_from_unix_ms(latest_time)
        df = binance_get_all_orders_by_pair(binance_client, pair_name, pair_startTime)
        df.rename(columns={'type':'orderType'}, inplace=True)
        df.to_sql("orders", binance_dbms.db_engine.connect(), if_exists="append", index=False)
        return ["Added "+pair_name+" !!"]
    else:
        return ["Provide both Pair and Start Date!"]

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=False)