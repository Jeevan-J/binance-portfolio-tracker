from ipaddress import collapse_addresses
import pandas as pd
import calendar
from datetime import datetime, timedelta, date

def binance_clean_assets(assets):
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
    all_ticker_values = pd.DataFrame(binance_client.get_symbol_ticker())
    all_ticker_values['price'] = all_ticker_values['price'].map(float)
    all_ticker_values.rename(columns={'price':'USDT Value','symbol':'Symbol'}, inplace=True)
    assets['Symbol'] = assets['Asset']+"USDT"
    assets = assets.merge(all_ticker_values, on='Symbol', how='left')
    assets.fillna(0.0)
    assets['USDT Value'] = ((assets['Spot Value']+assets['Locked Value'])*assets['USDT Value']).map(lambda x:round(x,6))
    assets.drop(columns=['Symbol','Locked Value'], inplace=True)
    return assets

def get_unix_ms_from_date(date):
    return int(calendar.timegm(date.timetuple()) * 1000 + date.microsecond/1000)

def get_date_from_unix_ms(unix):
    return datetime.fromtimestamp(unix/1000)

def binance_get_all_orders_by_pair(client, symbol, startTime):
    df = pd.DataFrame(client.get_all_orders(symbol=symbol, limit=1000, startTime=get_unix_ms_from_date(startTime)))
    while len(df)>=1000:
        startTime = get_date_from_unix_ms(df.loc[-1,'time'])
        temp_df = pd.DataFrame(client.get_all_orders(symbol=symbol, limit=1000, startTime=get_unix_ms_from_date(startTime)))
        df.append(temp_df, ignore_index=True)
    return df

def binance_update_aggregate_with_current_price(client, df):
    lastPrice = []
    for symbol in df['symbol']:
        lastPrice.append(float(client.get_ticker(symbol=symbol)['lastPrice']))
    df['Current Price'] = lastPrice
    df['Average USDT Price'] = (df['Total Invested USDT']/df['Asset Quantity']).map(lambda x:round(x,4))
    df['Total PNL'] = (df['Asset Quantity']*(df['Current Price'] - df['Average USDT Price'])).map(lambda x:round(x,4))
    df['Current Price'] = df['Current Price'].map(lambda x:round(x,4))
    df['Asset Quantity'] = df['Asset Quantity'].map(lambda x:round(x,4))
    df['Total Invested USDT'] = df['Total Invested USDT'].map(lambda x:round(x,4))
    df.rename(columns={'symbol':'Pair'}, inplace=True)
    return df