from engine.dataGenerator.order import Order
import random

class MarketTaker:
    def __init__(self, starting_price=100.0, buySellRatio=0.5, minSpread=0, maxSpread=0.05, maxqty=1000.0, lamdaQty=10.0):
        self.last_price = starting_price
        self.buySellRatio = buySellRatio
        self.minSpread = minSpread
        self.maxSpread = maxSpread
        self.maxqty = maxqty
        self.lamdaQty = lamdaQty

    def send_order(self, orderBook, order):
        orderBook.place_order(order)
    
    def send_random_order(self, orderBook):
        side = random.choices(["buy", "sell"], weights=[self.buySellRatio, 1 - self.buySellRatio])[0]
        best_ask = orderBook.best_ask()
        best_bid = orderBook.best_bid()

        if side == "buy":
            reference = best_ask if best_ask is not None else (best_bid if best_bid is not None else self.last_price)
            price = reference * (1 + random.uniform(self.minSpread, self.maxSpread))
        elif side == "sell":
            reference = best_bid if best_bid is not None else (best_ask if best_ask is not None else self.last_price)
            price = reference * (1 - random.uniform(self.minSpread, self.maxSpread))

        price = max(price, 0.01)
        qty = max(0.0001, min(random.expovariate(1/self.lamdaQty), self.maxqty))
        self.last_price = price  # Update last price
        
        order = Order(side=side, price=price, quantity=qty)
        return orderBook.place_order(order)