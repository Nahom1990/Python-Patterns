# infrastructure/adapters/postgres_repository.py
from Architecture.Hexagonal_architecture.domain.entities import Order, OrderStatus
from Architecture.Hexagonal_architecture.domain.ports import OrderRepositoryPort

class PostgresOrderRepositoryAdapter(OrderRepositoryPort):
    def __init__(self, db_session) -> None:
        self.db = db_session

    async def get_by_id(self, order_id: str) -> Order | None:
        # Talks to real SQL database using session
        row = await self.db.fetch_one("SELECT * FROM orders WHERE id = :id", {"id": order_id})
        if not row:
            return None
        return Order(id=row["id"], amount=row["amount"], status=OrderStatus(row["status"]))

    async def save(self, order: Order) -> None:
        await self.db.execute(
            "UPDATE orders SET status = :status WHERE id = :id",
            {"status": order.status.value, "id": order.id}
        )

