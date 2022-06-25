"""
This module contains the spot page of the dashboard.

Returns:
    function: to create the layout of the spot page.
"""

import pathlib

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from utils import header, make_dash_table
from functions import binance_clean_assets, binance_add_usdt_to_assets
from functions import binance_update_aggregate_with_current_price


# get relative data folder
PATH = pathlib.Path(__file__).parent

assets_style_cell_conditional=[
    {
        'if': {'column_id': c},
        'textAlign': 'left'
    } for c in ['Asset']
]

def create_layout(app, binance_client, binance_dbms):
    """
    This is the layout function of the spot page.

    Args:
        app (Dash): Dash application object.
        binance_client (binance.client.Client): Binance client object.
        binance_dbms (BinanceDB): Local Binance database object.

    Returns:
        html.Div: html.Div object containing the layout of the spot page.
    """
    balances = binance_client.get_account()['balances']
    balances = binance_clean_assets(balances)
    balances = binance_add_usdt_to_assets(binance_client, balances)

    asset_dist_fig = go.Figure(
        go.Pie(
            labels=balances['Asset'],
            values=balances['USDT Value'],
            showlegend=False
        )
    )
    asset_dist_fig.update_traces(textposition='inside')
    asset_dist_fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    asset_dist_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    aggregated_data = binance_update_aggregate_with_current_price(
        binance_client,
        binance_dbms.get_aggregated_data()
    )

    # Page Layouts
    return html.Div([
        html.Div([header(app)]),
        # Page 1
        html.Div([
            html.Div([
                html.Div(
                    [
                        html.H6(["Spot Positions"], className="subtitle padded"),
                        html.Table(
                            make_dash_table(
                                balances,
                                style_cell_conditional=assets_style_cell_conditional)
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.H6(["Asset Distribution"], className="subtitle padded"),
                        dcc.Graph(
                            id='asset-distribution',
                            figure=asset_dist_fig
                        )
                    ],
                    className="six columns",
                ),
            ], className="row"),
            html.Div([
                html.Div(
                    [
                        html.H6(["Add Pair"], className="subtitle padded"),
                        html.Div([
                            html.Div([
                                    dbc.Label("Pair",
                                              width="auto",
                                              style={"margin-right": "16px"}),
                                    dbc.Input(id="add-pair-name",
                                              type="text",
                                              placeholder="Enter Pair (BNBUSDT/BTCUSDT)"),
                                ],
                                className="five columns",
                                style={"display": "flex", "align-items": "baseline"}),
                            html.Div([
                                    dbc.Label("Start Date",
                                            width="auto",
                                            style={"margin-right": "16px"}),
                                    dbc.Input(id="add-pair-startTime",
                                            type="date",
                                            placeholder="Select a start date for tracking"),
                                ],
                                className="five columns",
                                style={"display": "flex", "align-items": "baseline"}),
                            html.Div([
                                    html.Button("Add", id="add-pair-submit", n_clicks=0)
                                ],
                                className="two columns"),
                        ], className="row padded"),
                        dcc.Loading(html.Div(id='add-pair-out'), type='circle'),
                        html.Br(),
                        html.H6(["Total PnL Table"], className="subtitle padded"),
                        html.Table(
                            make_dash_table(
                                aggregated_data,
                                style_cell_conditional=assets_style_cell_conditional)
                            ),
                    ],
                    className="twelve columns",
                ),
            ], className="row"),
        ], className="sub_page")
    ], className="page")
    