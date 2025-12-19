from engine.dataGenerator.order import Order
import random

class MarketMaker:
    def __init__(self, starting_price=100.0):
        self.last_price = starting_price

    def send_order(self, orderBook, order):
        orderBook.place_order(order)
    
    def send_random_order(self, orderBook):
        side = random.choices(["buy", "sell"], weights=[0.5, 0.5])[0]
        best_ask = orderBook.best_ask()
        best_bid = orderBook.best_bid()
        
        if side == "buy":
            reference = best_bid if best_bid is not None else (best_ask if best_ask is not None else self.last_price)
            price = reference * (1 - random.uniform(0.001, 0.02))
        else:
            reference = best_ask if best_ask is not None else (best_bid if best_bid is not None else self.last_price)
            price = reference * (1 + random.uniform(0.001, 0.02))

        price = max(price, 0.01)
        qty = max(0.0001, min(random.expovariate(1/10), 1000))
        self.last_price = price  # Update last price

        order = Order(side=side, price=price, quantity=qty)
        return orderBook.place_order(order)
