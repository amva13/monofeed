"""
TODO

In production would have these in separate files and use factory method.
"""

from decimal import Decimal
from schema import Tick
from mq import TickQueue
from db import consoleDB, csvDB
from processes import TickWriterDefaultEnqueueThread, TickWriterDefaultDequeueThread

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
            Tick(t.exchange, t.symbol, t.bid, t.ask, t.timestamp, receipt_timestamp)
            print(f'Ticker received at {timestamp}: {t}')
        tickerWrite(t, receipt_timestamp)

        
class MQTickerWriter(TickerWriter):
    
    def __init__(self, max_q_size=100):
        try:
            super().__init__()
        except:
            pass
        self.mq = TickQueue(max_size=max_q_size)
        # self.db = consoleDB()
        self.db = csvDB({
            "path":"test_path/file.csv",  # TODO: eliminate hard-coded. Judged to be ok for now given it's a local csv writer prototype
            "type":Tick,
            "fields":["exchange","symbol","bid","ask","timestamp","time_received"],
        })
        self.consumer = TickWriterDefaultDequeueThread(queue=self.mq, db=self.db)
        self.consumer.start()
        
    def getWriter(self):
        async def callback(t, timestamp):
            if t.timestamp is not None:
                assert isinstance(t.timestamp, float)
            assert isinstance(t.exchange, str)
            assert isinstance(t.bid, Decimal)
            assert isinstance(t.ask, Decimal)
            print(f'Ticker received at {timestamp}: {t}')
            print("writing...")
            tick = Tick(t.exchange, t.symbol, t.bid, t.ask, t.timestamp, timestamp)
            t = TickWriterDefaultEnqueueThread(tick, self.mq)
            t.start()
            t.join()
            print(f"Finished enqueueing write of tick {tick.as_dict()}")
        return callback 