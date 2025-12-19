import heapq
from collections import deque
from typing import Deque, Dict, List, Optional
from engine.dataGenerator.order import Order

class OrderBook:
    def __init__(self, defaultPrice: float = 100.0):
        # price -> deque of orders
        self.bids: Dict[float, Deque[Order]] = {}
        self.asks: Dict[float, Deque[Order]] = {}

        # heaps for best prices
        self.bid_prices: List[float] = []  # max-heap using negative prices
        self.ask_prices: List[float] = []  # min-heap

        self.last_price = defaultPrice  # Track last traded/reference price
        self.defaultPrice = defaultPrice

    # ------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------
    def _add_price_level(self, price: float, book: Dict[float, Deque[Order]], heap: List[float], is_bid=False):
        if price not in book:
            book[price] = deque()
            if is_bid:
                heapq.heappush(heap, -price)  # max-heap trick
            else:
                heapq.heappush(heap, price)

    def _remove_price_level(self, price: float, book: Dict[float, Deque[Order]], heap: List[float], is_bid=False):
        del book[price]
        if is_bid:
            heap.remove(-price)
            heapq.heapify(heap)
        else:
            heap.remove(price)
            heapq.heapify(heap)

    def best_bid(self) -> Optional[float]:
        return -self.bid_prices[0] if self.bid_prices else self.last_price

    def best_ask(self) -> Optional[float]:
        return self.ask_prices[0] if self.ask_prices else self.last_price

    # ------------------------------------------------------------
    # Order insertion
    # ------------------------------------------------------------
    def place_order(self, order: Order):
        if order.side == "buy":
            return self._handle_buy(order)
        else:
            return self._handle_sell(order)

    # ------------------------------------------------------------
    # Buy order matching
    # ------------------------------------------------------------
    def _handle_buy(self, order: Order):
        trades = []
        while order.quantity > 0 and self.ask_prices:
            best_ask = self.best_ask()
            if best_ask is None or order.price < best_ask:
                break

            ask_queue = self.asks[best_ask]
            best_order = ask_queue[0]

            traded_qty = min(order.quantity, best_order.quantity)
            trades.append((order.order_id, best_order.order_id, best_ask, traded_qty))
            self.last_price = best_ask  # Update last price on trade

            order.quantity -= traded_qty
            best_order.quantity -= traded_qty

            if best_order.quantity == 0:
                ask_queue.popleft()
                if not ask_queue:
                    self._remove_price_level(best_ask, self.asks, self.ask_prices, is_bid=False)

        if order.quantity > 0:
            self._add_price_level(order.price, self.bids, self.bid_prices, is_bid=True)
            self.bids[order.price].append(order)

        return trades

    # ------------------------------------------------------------
    # Sell order matching
    # ------------------------------------------------------------
    def _handle_sell(self, order: Order):
        trades = []
        while order.quantity > 0 and self.bid_prices:
            best_bid = self.best_bid()
            if best_bid is None or order.price > best_bid:
                break

            bid_queue = self.bids[best_bid]
            best_order = bid_queue[0]

            traded_qty = min(order.quantity, best_order.quantity)
            trades.append((order.order_id, best_order.order_id, best_bid, traded_qty))
            self.last_price = best_bid  # Update last price on trade

            order.quantity -= traded_qty
            best_order.quantity -= traded_qty

            if best_order.quantity == 0:
                bid_queue.popleft()
                if not bid_queue:
                    self._remove_price_level(best_bid, self.bids, self.bid_prices, is_bid=True)

        if order.quantity > 0:
            self._add_price_level(order.price, self.asks, self.ask_prices, is_bid=False)
            self.asks[order.price].append(order)

        return trades

    def print_orderbook(self):
        print("\n=== ORDER BOOK ===")

        # ----- Asks -----
        print("\nAsks (price ↑):")
        for price in sorted(self.asks.keys()):
            levels = self.asks[price]
            qty_sum = sum(o.quantity for o in levels)
            print(f"  {price:.2f}  | total={qty_sum:.4f}")
            for o in levels:
                print(f"      id={o.order_id} qty={o.quantity:.4f}")

        # ----- Bids -----
        print("\nBids (price ↓):")
        for price in sorted(self.bids.keys(), reverse=True):
            levels = self.bids[price]
            qty_sum = sum(o.quantity for o in levels)
            print(f"  {price:.2f}  | total={qty_sum:.4f}")
            for o in levels:
                print(f"      id={o.order_id} qty={o.quantity:.4f}")

        print("==================\n")


# Example usage
if __name__ == "__main__":
    book = OrderBook()

    book.place_order(Order("B1", "buy", 100, 10))
    book.place_order(Order("B2", "buy", 101, 5))
    book.place_order(Order("S1", "sell", 99, 3))
    book.place_order(Order("S2", "sell", 101, 10))

    print("Best Bid:", book.best_bid())
    print("Best Ask:", book.best_ask())
