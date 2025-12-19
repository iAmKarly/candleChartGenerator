from engine.dataGenerator.order import Order
from engine.dataGenerator.orderBook import OrderBook
from engine.dataGenerator.agents.marketTaker import MarketTaker
from engine.dataGenerator.agents.marketMaker import MarketMaker
from engine.dataGenerator.candleBuilder import CandleBuilder
import pandas as pd

class MarketEngine:
    def __init__(self):
        self.running = False
        self.orderBook = OrderBook()
        self.taker = MarketTaker()
        self.maker = MarketMaker()
        self.candleBuilder = CandleBuilder()
        self.candles = pd.DataFrame()
        self.numTrades = 10
        self.time = 0

    def start(self, startPrice: float = 100.0, startQuantity: float = 50.0):
        self.running = True
        print("Market Engine started.")
        order = Order(side="buy", price=startPrice-1.0, quantity=startQuantity)
        self.orderBook.place_order(order)
        order = Order(side="sell", price=startPrice+1.0, quantity=startQuantity)
        self.orderBook.place_order(order)
        

    def stop(self):
        self.running = False

    def step(self):
        if not self.running:
            return None

        self.time += 1
        candle = self.candleBuilder.getRandomNextCandleRow(self.time, self.orderBook, self.taker, self.maker, self.numTrades)

        self.candles = pd.concat([self.candles, pd.DataFrame(candle)], ignore_index=True)  
        return candle
        
        
if __name__ == "__main__":
    engine = MarketEngine()
    engine.start()
    for _ in range(10):
        candle = engine.step()
        print(candle)
    engine.stop()