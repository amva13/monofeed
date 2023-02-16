from datetime import datetime
import pytz
from decimal import Decimal

class Tick:
    def __init__(self, exchange, symbol, bid, ask, timestamp, time_received, timezone=None):
        assert isinstance(symbol,str)
        assert isinstance(bid,Decimal)
        assert isinstance(ask,Decimal)
        assert isinstance(timestamp,float)
        assert isinstance(time_received,float)
        assert isinstance(exchange,str)
        self.exchange = exchange
        self.symbol = symbol
        self.bid = bid
        self.ask = ask
        self.timestamp = timestamp
        self.time_received = time_received
        self.tz = timezone if timezone is not None else "America/New_York"
        
    def timestampConvert(self, ts):
        tz = pytz.timezone(self.tz)
        return datetime.fromtimestamp(ts).astimezone(tz)
        
    def getTS(self):
        return self.timestampConvert(self.timestamp)
    
    def getTSReceived(self):
        return self.timestampConvert(self.time_received)
    
    def as_dict(self):
        return {
            "exchange": self.exchange,
            "symbol": self.symbol,
            "bid": self.bid,
            "ask": self.ask,
            "timestamp": self.timestampConvert(self.timestamp),
            "time_received": self.timestampConvert(self.time_received)
        }

        
class Query(dict):
    
    def __init__(self, params=None):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented __init__()")
    

class RangeQuery(Query):
    
    def __init__(self, params=None):
        params = {} if params is None else params
        self.format = "%m/%d/%y" if "format" not in params else params["format"]
        assert isinstance(self.format, str)
    
    def addFrom(self, dt):
        assert isinstance(dt, str)
        self["from"]=datetime.strptime(dt, self.format)
        
    def addTo(self, dt):
        assert isinstance(dt, str)
        self["to"]=datetime.strptime(dt,self.format)

    def addExchange(self, ex):
        assert isinstance(ex, str)
        self["exchange"]=ex
        
    def addSymbol(self, symbol):
        assert isinstance(symbol, str)
        self["symbol"]=symbol