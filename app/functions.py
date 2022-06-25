"""
This is a helper functions module for binance aggregating functions.

Returns:
    methods: functions for aggregating binance data.
"""
from datetime import datetime
import calendar

import pandas as pd

def binance_clean_assets(assets):
    """
    This is a helper function that cleans the assets dataframe.

    Args:
        assets (pd.DataFrame): Assets dataframe.

    Returns:
        pd.DataFrame: Cleaned assets dataframe.
    """
    out = []
    for asset in assets:
        if (float(asset['free'])>0) or (float(asset['locked'])>0):
            out.append(asset)
    out = pd.DataFrame(out)
    out['free'] = out['free'].map(float).map(lambda x:round(x,6))
    out['locked'] = out['locked'].map(float).map(lambda x:round(x,6))
    out.rename(columns={'asset':'Asset','free':'Spot Value', 'locked':'Locked Value'}, inplace=True)
    return out

def binance_add_usdt_to_assets(binance_client, assets):
    """
    This adds USDT column to the assets dataframe and renames columns.

    Args:
        binance_client (binance.client.Client): Binance client object.
        assets (pd.DataFrame): Assets dataframe.

    Returns:
        pd.DataFrame: Assets dataframe with USDT column.
    """
    all_ticker_values = pd.DataFrame(binance_client.get_symbol_ticker())
    all_ticker_values['price'] = all_ticker_values['price'].map(float)
    all_ticker_values.rename(columns={'price':'USDT Value','symbol':'Symbol'}, inplace=True)
    assets['Symbol'] = assets['Asset']+"USDT"
    assets = assets.merge(all_ticker_values, on='Symbol', how='left')
    assets.fillna(0.0)
    assets['USDT Value'] = (
            (assets['Spot Value']+assets['Locked Value'])*assets['USDT Value']
        ).map(lambda x:round(x,6))
    assets.drop(columns=['Symbol','Locked Value'], inplace=True)
    return assets

def get_unix_ms_from_date(date):
    """
    Converts a datetime object to unix timestamp in milliseconds.

    Args:
        date (datetime): date object.

    Returns:
        int: timestamp in milliseconds.
    """
    return int(calendar.timegm(date.timetuple()) * 1000 + date.microsecond/1000)

def get_date_from_unix_ms(unix):
    """
    Converts a unix timestamp in milliseconds to datetime object.

    Args:
        unix (int): timestamp in milliseconds.

    Returns:
        datetime: datetime object.
    """
    return datetime.fromtimestamp(unix/1000)

def binance_get_all_orders_by_pair(client, symbol, start_time):
    """
    Gets all orders for a given symbol and start time.

    Args:
        client (binance.client.Client): Binance client object.
        symbol (str): symbol to get orders for.
        start_time (datetime): date to start getting orders from.

    Returns:
        pd.DataFrame: a dataframe of all orders for a given symbol and start time.
    """
    orders_df = pd.DataFrame(
        client.get_all_orders(
            symbol=symbol,
            limit=1000,
            startTime=get_unix_ms_from_date(start_time)
        )
    )
    while len(orders_df)>=1000:
        start_time = get_date_from_unix_ms(orders_df.loc[-1,'time'])
        temp_df = pd.DataFrame(
            client.get_all_orders(
                symbol=symbol,
                limit=1000,
                startTime=get_unix_ms_from_date(start_time)
            )
        )
        orders_df.append(temp_df, ignore_index=True)
    return orders_df

def binance_update_aggregate_with_current_price(client, portfolio_df):
    """
    Adds current price to the portfolio dataframe.

    Args:
        client (binance.client.Client): Binance client object.
        portfolio_df (pd.DataFrame): portfolio dataframe.

    Returns:
        pd.DataFrame: portfolio dataframe with current price.
    """
    last_price = []
    for symbol in portfolio_df['symbol']:
        last_price.append(float(client.get_ticker(symbol=symbol)['lastPrice']))
    portfolio_df['Current Price'] = last_price
    portfolio_df['Average USDT Price'] = (
            portfolio_df['Total Invested USDT']/portfolio_df['Asset Quantity']
        ).map(lambda x:round(x,4))
    portfolio_df['Total PNL'] = (
            portfolio_df['Asset Quantity']
            *
            (portfolio_df['Current Price'] - portfolio_df['Average USDT Price'])
        ).map(lambda x:round(x,4))
    portfolio_df['Current Price'] = portfolio_df['Current Price'].map(lambda x:round(x,4))
    portfolio_df['Asset Quantity'] = portfolio_df['Asset Quantity'].map(lambda x:round(x,4))
    portfolio_df['Total Invested USDT'] = portfolio_df['Total Invested USDT'].map(
        lambda x:round(x,4)
    )
    portfolio_df.rename(columns={'symbol':'Pair'}, inplace=True)
    return portfolio_df
