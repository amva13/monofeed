"""
Run monofeed.py to obtain some data locally. Then you can run main.py for basic tests.
"""

from querydb import CsvDBQuery
from db import csvDB
from schema import RangeQuery, Tick
import pandas as pd

if __name__ == "__main__":
    query = RangeQuery()
    dtTo1 = "12/13/23"
    dtFrom1 = "12/13/22"
    ex1 = "COINBASE"
    sym1 = "ETH-USDT"
    db = csvDB({
        "path":"test_path/file.csv", 
        "type":Tick,
        "fields":["exchange","symbol","bid","ask","timestamp","time_received"],
    })
    dbquery = CsvDBQuery(db)
    # query 1
    query.addFrom(dtFrom1)
    query.addTo(dtFrom1)
    query.addExchange(ex1)
    query.addSymbol(sym1)
    original_df = db.read()
    df = dbquery.select(query)
    original_df["timestamp"] = pd.to_datetime(original_df["timestamp"])
    assert len(df[df[df.symbol != "ETH-USDT"]]) == 0
    dftest1 = original_df[original_df["symbol"]== "ETH-USDT"]
    dftest1 = dftest1[dftest1["exchange"] == "COINBASE"]
    dftest1 = dftest1[dftest1["timestamp"].dt.date <= query["to"].date()]
    dftest1 = dftest1[dftest1["timestamp"].dt.date >= query["from"].date()]
    assert df.equals(dftest1)

    # query 2
    query.addSymbol("BTC-USDT")
    df = dbquery.select(query)
    assert len(df[df.symbol != "BTC-USDT"]) == 0
    dftest2 = original_df[original_df["symbol"]== "ETH-USDT"]
    dftest2 = dftest2[dftest2["exchange"] == "COINBASE"]
    dftest2 = dftest2[dftest2["timestamp"].dt.date <= query["to"].date()]
    dftest2 = dftest2[dftest2["timestamp"].dt.date >= query["from"].date()] 
    assert df.equals(dftest2)
    
    # query 3
    query.addSymbol("dummyval")
    df = dbquery.select(query)
    assert len(df) == 0
    
    # query 4
    del query["symbol"]
    query.addTo("12/14/22")
    df = dbquery.select(query)
    assert len(df) == 0
    
    # query 5
    del query["to"]
    query.addExchange("dummyval")
    df = dbquery.select(query)
    assert len(df) == 0

    print("ALL TESTS PASSED!")