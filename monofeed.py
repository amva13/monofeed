from cryptofeed import FeedHandler
from cryptofeed.defines import TICKER
from cryptofeed.exchanges import Coinbase
from writers import MQTickerWriter as writer

class MonoFeed:
    EXCHANGES = {
        "CB": Coinbase
    }
    
    DEFINES = {
        "TICKER": TICKER,
    }
    
    WRITERS = {
        TICKER: None,
    }
    
    def __init__(self):
        self.feedHandler = FeedHandler()
        self.writer = writer()
        self.WRITERS[TICKER] = self.writer.getWriter()
        
    def addCryptoFeed(self, exchange, args_dict):
        self.feedHandler.add_feed(self.EXCHANGES[exchange](**args_dict))
        
    def addFeed(self, symbols, defines = ["TICKER"], exchanges = ["CB"]):
        if not isinstance(symbols, str):
            assert isinstance(symbols,list)
        else:
            symbols = [symbols]
        for ex in exchanges:
            if ex not in self.EXCHANGES:
                all = ', '.join(self.EXCHANGES.keys())
                raise ValueError(f"Exchange {ex} is not a supported exchange symbol, try one of the following: {all}")
            for d in defines:
                if d not in self.DEFINES:
                    all = ', '.join(self.DEFINES.keys())
                    raise ValueError(f"Define {d} is not a supported query define symbol, try one of the following: {all}")
                self.addCryptoFeed(ex, {"symbols": symbols, "channels":[self.getDefine(d)], "callbacks":self.WRITERS})
                
    def run(self):
        self.runForeverSingleThread()
    
    def runForeverSingleThread(self):
        self.feedHandler.run()

    def getDefine(cls, d):
        return cls.DEFINES.get(d)
    
if __name__ == '__main__':
    fh = MonoFeed()
    symbols = ['BTC-USDT', 'ETH-USDT']
    fh.addFeed(symbols)
    fh.run()