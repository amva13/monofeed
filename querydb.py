from db import csvDB
import pandas as pd
from schema import RangeQuery, Tick

class AbstractQuery:
    
    def __init__(self, db):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented __init__()")
    
    def select(self, query=None):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented select()")
    
    
class CsvDBQuery(AbstractQuery):
    _QUERIES = [
        RangeQuery
    ]
    
    def __init__(self, db):
        if not isinstance(db, csvDB):
            raise TypeError("CsvDBQuery can only take a csvDB as input")
        self.db = db
        
    def select(self, query=None):
        if query is None:
            raise ValueError("did not include query specification")
        assert type(query) in self._QUERIES
        df = self.db.read()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        if "exchange" in query:
            df = df[df["exchange"] == query["exchange"]]
        if "symbol" in query:
            df = df[df["symbol"] == query["symbol"]]
            
        if "to" in query:
            df = df[df["timestamp"].dt.date <= query["to"].date()]
            
        if "from" in query:
            df = df[df["timestamp"].dt.date >= query["from"].date()]
            
        return df
        
        
if __name__ == "__main__":
    query = RangeQuery()
    query.addFrom("12/31/22")
    query.addTo("12/31/23")
    query.addExchange("COINBASE")
    query.addSymbol("ETH-USDT")
    db = csvDB({
        "path":"test_path/file.csv", 
        "type":Tick,
        "fields":["exchange","symbol","bid","ask","timestamp","time_received"],
    })
    dbquery = CsvDBQuery(db)
    df = dbquery.select(query)
    print("should get all rows with ETH-USDT ...")
    print(df.head())
    print("done...")
    print()
    query.addSymbol("BTC-USDT")
    print("should get all rows with BTC-USDT ...")
    df = dbquery.select(query)
    print(df.head())
    print("done ...")
    print()
    query.addFrom("12/31/24")
    print("should give nothing due to date")
    df = dbquery.select(query)
    print(df.head())
    print("done...")
    