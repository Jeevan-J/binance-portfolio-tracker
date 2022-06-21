from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://username:password@localhost/{DB}',
        # POSTGRESQL: 'postgresql://username:password@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://username:password@hostname:port/{DB}'
    }
    
    
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            self.engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(self.engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")
            
    def create_db_tables(self):
        metadata = MetaData()
        orders = Table(ORDERS, metadata,
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
        
        pairs = Table(PAIRS, metadata,
                        Column('symbol', String, primary_key=True),
                        Column('startTime', DateTime)
                      )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)
    
    def get_last_time_for_symbol(self, symbol):
        db_engine = create_engine(self.engine_url)
        conn = db_engine.connect()
        QUERY = """
        select 
            symbol, time
        from 
            orders o 
        where 
            o.symbol = "{}"   
        """
        df = pd.read_sql_query(QUERY.format(symbol), conn)
        conn.close()
        if df.empty:
            return None
        else:
            return max(df['time'])
        
    def get_aggregated_data(self):
        db_engine = create_engine(self.engine_url)
        conn = db_engine.connect()        
        QUERY = """
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
        df = pd.read_sql_query(QUERY, conn)
        conn.close()
        if df.empty:
            return None
        else:
            return df
        