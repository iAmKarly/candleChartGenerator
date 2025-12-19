from engine.dataGenerator.order import Order
from engine.dataGenerator.orderBook import OrderBook
from engine.dataGenerator.agents.marketTaker import MarketTaker
from engine.dataGenerator.agents.marketMaker import MarketMaker
from engine.dataGenerator.candleBuilder import CandleBuilder
from engine.dataGenerator.chart import Chart
import random

    
if __name__ == "__main__":
    orderBook = OrderBook()
    taker = MarketTaker()
    maker = MarketMaker()
    candleBuilder = CandleBuilder()

    order = Order(side="buy", price=99.0, quantity=50)
    orderBook.place_order(order)
    order = Order(side="sell", price=101.0, quantity=50)
    orderBook.place_order(order)

    candles = []
 
    for time in range(200):
        candle = candleBuilder.getRandomNextCandleObj(time, orderBook, taker, maker, 10)
        candles.append(candle)

    chart = Chart() 
    chart.plot_instant_web(candles)
