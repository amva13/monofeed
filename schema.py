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