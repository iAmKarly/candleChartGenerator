from engine.dataGenerator.candle import Candle
import pandas as pd
import random

class CandleBuilder:
    def __init__(self):
        self.prev_close = None

    def make_candle_obj(self, time, orderBook, trades_in_loop):
        best_bid = orderBook.best_bid()
        best_ask = orderBook.best_ask()

        # fallback if empty book
        mid = (best_bid + best_ask) / 2 if best_bid and best_ask else self.prev_close
        
        # OPEN
        if self.prev_close is None:
            open = mid
        else:
            open = self.prev_close

        # HIGH & LOW (based on book movement this iteration)
        candidates = [open]
        if best_bid: candidates.append(best_bid)
        if best_ask: candidates.append(best_ask)
        high = max(candidates)
        low = min(candidates)

        # CLOSE = mid-price or last trade price
        close = mid
        if trades_in_loop:
            # use last trade price if any trades occurred
            close = trades_in_loop[-1][2]

        # VOLUME = sum of quantities this loop
        volume = sum(t[3] for t in trades_in_loop)

        # update and return candle
        self.prev_close = close

        return Candle(time, open, high, low, close, volume)
  
    def make_candle_row(self, time, orderBook, trades_in_loop):
        best_bid = orderBook.best_bid()
        best_ask = orderBook.best_ask()

        # fallback if empty book
        mid = (best_bid + best_ask) / 2 if best_bid and best_ask else self.prev_close
        
        # OPEN
        if self.prev_close is None:
            open = mid
        else:
            open = self.prev_close

        # HIGH & LOW (based on book movement this iteration)
        candidates = [open]
        if best_bid: candidates.append(best_bid)
        if best_ask: candidates.append(best_ask)
        high = max(candidates)
        low = min(candidates)

        # CLOSE = mid-price or last trade price
        close = mid
        if trades_in_loop:
            # use last trade price if any trades occurred
            close = trades_in_loop[-1][2]

        # VOLUME = sum of quantities this loop
        volume = sum(t[3] for t in trades_in_loop)

        # update and return candle
        self.prev_close = close

        candle_row = {
            'time': time,
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume
        }

        candle_row_df = pd.DataFrame([candle_row])
        return candle_row_df

    def getRandomNextCandleObj(self, time, orderBook, taker, maker, numTrades):
        trades = []

        for _ in range(numTrades):
            if random.random() < 0.3:
                trades.extend(maker.send_random_order(orderBook))
            else:
                trades.extend(taker.send_random_order(orderBook))

        candle = self.make_candle_obj(time, orderBook, trades)
        return candle

    def getRandomNextCandleRow(self, time, orderBook, taker, maker, numTrades):
        trades = []

        for _ in range(numTrades):
            if random.random() < 0.3:
                trades.extend(maker.send_random_order(orderBook))
            else:
                trades.extend(taker.send_random_order(orderBook))

        candle = self.make_candle_row(time, orderBook, trades)
        return candle