from dataclasses import dataclass, field
import uuid

@dataclass
class Order:
    side: str      # "buy" or "sell"
    price: float
    quantity: float
    order_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    