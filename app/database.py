"""
Database Helper Class for storing Binance Orders data
"""
from sqlite3 import OperationalError
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, MetaData

import pandas as pd

# Global Variables
SQLITE                  = 'sqlite'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'

# Table Names
ORDERS           = 'orders'
PAIRS            = 'pairs'

class BinanceDB:
    """
    This class is used to create a database connection and execute queries.
    """
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://username:password@localhost/{DB}',
        # POSTGRESQL: 'postgresql://username:password@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://username:password@hostname:port/{DB}'
    }

    db_engine = None

    def __init__(self, dbtype, dbname=''):
        dbtype = dbtype.lower()
        dbtypes = list(self.DB_ENGINE.keys())
        if dbtype in dbtypes:
            self.engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(self.engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        """
        Creates the database tables if they do not exist.
        """
        metadata = MetaData()
        Table(ORDERS, metadata,
                Column('orderId',Integer, primary_key=True),
                Column('cummulativeQuoteQty',Integer),
                Column('executedQty',Integer),
                Column('icebergQty',Integer),
                Column('orderListId',Integer),
                Column('origQty',Integer),
                Column('origQuoteOrderQty',Integer),
                Column('price',Integer),
                Column('stopPrice',Integer),
                Column('clientOrderId',String),
                Column('isWorking',String),
                Column('side',String),
                Column('status',String),
                Column('symbol',String),
                Column('orderType',String),
                Column('symbol',String),
                Column('timeInForce',String),
                Column('time',DateTime),
                Column('updateTime',DateTime)
            )
        Table(PAIRS, metadata,
                Column('symbol', String, primary_key=True),
                Column('startTime', DateTime)
            )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except OperationalError as error:
            print("Error occurred during Table creation!")
            print(error)

    def get_last_time_for_symbol(self, symbol):
        """
        Returns the last order time for a symbol from the database.
        """
        db_engine = create_engine(self.engine_url)
        conn = db_engine.connect()
        query = """
        select 
            symbol, time
        from 
            orders o 
        where 
            o.symbol = "{}"   
        """
        latest_order_record = pd.read_sql_query(query.format(symbol), conn)
        conn.close()
        if latest_order_record.empty:
            return None
        return max(latest_order_record['time'])

    def get_aggregated_data(self):
        """
        Returns the aggregated data from the database.
        """
        db_engine = create_engine(self.engine_url)
        conn = db_engine.connect()
        query = """
        SELECT 
            symbol, SUM(executedqty*sign) AS "Asset Quantity", SUM(cummulativequoteqty*sign) AS "Total Invested USDT"
        FROM 
            (SELECT 
                symbol, executedQty, cummulativeQuoteQty,
                CASE side 
                WHEN 'SELL' THEN -1
                WHEN 'BUY' THEN 1
                END AS sign
            FROM orders)
        GROUP BY symbol
        """
        aggregated_df = pd.read_sql_query(query, conn)
        conn.close()
        if aggregated_df.empty:
            return None
        return aggregated_df
        