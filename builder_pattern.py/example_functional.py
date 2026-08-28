from dataclasses import dataclass, field


@dataclass
class Order:
    customer_id: int
    items: list[str]
    discount: float
    shipping_method: str
    payment_method: str
    total: float


def create_order(
    customer_id: int,
    items: list[str],
    discount: float = 0,
    shipping_method: str = "standard",
    payment_method: str = "card",
) -> Order:

    if not items:
        raise ValueError("Order must contain items")

    total = 100.0 * (1 - discount / 100)

    return Order(
        customer_id=customer_id,
        items=items,
        discount=discount,
        shipping_method=shipping_method,
        payment_method=payment_method,
        total=total,
    )


#use
order=create_order(1,["a","b"],1,"flight","card")
print(order)