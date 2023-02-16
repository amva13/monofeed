from datetime import datetime
from decimal import Decimal
import time

from cryptofeed import FeedHandler
from cryptofeed.defines import TICKER
from cryptofeed.exchanges import Coinbase


async def ticker(t, receipt_timestamp):
    if t.timestamp is not None:
        assert isinstance(t.timestamp, float)
    assert isinstance(t.exchange, str)
    assert isinstance(t.bid, Decimal)
    assert isinstance(t.ask, Decimal)
    print(f'Ticker received at {receipt_timestamp}: {t}')
    

fh = FeedHandler()

ticker_cb = {TICKER: ticker}


fh.add_feed(Coinbase(symbols=['BTC-USDT', 'ETH-USDT'], channels=[TICKER], callbacks=ticker_cb))

fh.run()
# time.sleep(10)
# fh.stop()