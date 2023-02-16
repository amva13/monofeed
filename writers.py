"""
TODO

In production would have these in separate files and use factory method.
"""

from decimal import Decimal

class AbstractWriter:
    def __init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented __init__(), it may be an abstract class, please inherit from it for implementations.")
    
class TickerWriter(AbstractWriter):
    
    def write(cls, args_dict):
        raise NotImplementedError(f"{cls.__class__.__name__} has not implemented its write() method.")
    
class TickerConsoleWriter(TickerWriter):
    pass
    
class AsyncTickerConsoleWriter(TickerConsoleWriter):

    def __init__(self):
        try:
            super().__init__() # currently fails ^, keeping inheritance for simplicity of building on upstream classes
        except:
            pass 
    
    async def write(t, receipt_timestamp):
        def tickerWrite(t, timestamp):
            if t.timestamp is not None:
                assert isinstance(t.timestamp, float)
            assert isinstance(t.exchange, str)
            assert isinstance(t.bid, Decimal)
            assert isinstance(t.ask, Decimal)
            print(f'Ticker received at {timestamp}: {t}')
        tickerWrite(t, receipt_timestamp)
        # if "t" not in args_dict or "receipt_timestamp" not in args_dict:
        #     raise ValueError(f"call to {cls.__class__.__name__}'s write() method is missing required arguments")
        # tickerWrite(**args_dict)
        