"""
An Event Bus works on the Pub-Sub model. 
When a producer fires an event onto the bus, the bus immediately 
pushes that event out to all active subscribers. 
If no one is listening, the event usually just vanishes into thin air.

A Queue works on the Producer-Consumer model. 
It holds onto the message safely in memory or disk until a 
consumer comes along, pulls it out, and deletes it."""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol, Set, Type, TypeVar, Self
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 1. EVENT CONTRACT (PROTOCOL)
class DomainEvent(Protocol):
    """Protocol that all domain events must satisfy."""
    @property
    def event_type(self) -> str: ...
    @property
    def event_id(self) -> str: ...


# 2. CONCRETE DOMAIN EVENTS
@dataclass(frozen=True)
class UserRegisteredEvent:
    user_id: str
    email: str
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def event_type(self) -> str:
        return "user.registered"


@dataclass(frozen=True)
class OrderPlacedEvent:
    order_id: str
    amount: float
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def event_type(self) -> str:
        return "order.placed"


# 3. HANDLER CONTRACT
E = TypeVar("E", bound=DomainEvent, contravariant=True)

class EventHandler(Protocol[E]):
    async def handle(self, event: E) -> None: ...


# 4. CONCRETE HANDLERS
class WelcomeEmailHandler:
    async def handle(self, event: UserRegisteredEvent) -> None:
        logging.info(f"[EmailHandler] Sending welcome email to {event.email}")
        await asyncio.sleep(0.1)


class AuditLogHandler:
    async def handle(self, event: DomainEvent) -> None:
        logging.info(f"[AuditLog] Captured event '{event.event_type}' (ID: {event.event_id})")


# 5. ENTERPRISE EVENT BUS IMPLEMENTATION
class AsyncEventBus:
    def __init__(self, max_concurrent_handlers: int = 10) -> None:
        self._handlers: Dict[str, Set[EventHandler[Any]]] = {}
        self._global_handlers: Set[EventHandler[Any]] = set()
        self._semaphore = asyncio.Semaphore(max_concurrent_handlers)

    def subscribe(self, event_type: str, handler: EventHandler[Any]) -> None:
        if event_type == "*":
            self._global_handlers.add(handler)
            return
        
        if event_type not in self._handlers:
            self._handlers[event_type] = set()
        self._handlers[event_type].add(handler)

    async def publish(self, event: DomainEvent) -> None:
        """Publishes an event to matching handlers concurrently with backpressure safety."""
        target_handlers = self._handlers.get(event.event_type, set()).union(self._global_handlers)
        
        if not target_handlers:
            logging.warning(f"No handlers registered for event '{event.event_type}'")
            return

        # Execute all matching handlers concurrently using asyncio.gather
        tasks = [
            asyncio.create_task(self._dispatch_safely(handler, event))
            for handler in target_handlers
        ]
        await asyncio.gather(*tasks)

    async def _dispatch_safely(self, handler: EventHandler[Any], event: DomainEvent) -> None:
        # Enforce concurrency limits using Semaphore
        async with self._semaphore:
            try:
                await handler.handle(event)
            except Exception as exc:
                logging.error(f"Error handling '{event.event_type}' in {handler}: {exc}")


# --- RUNNER ---
async def main_protocol() -> None:
    bus = AsyncEventBus(max_concurrent_handlers=5)

    email_handler = WelcomeEmailHandler()
    audit_handler = AuditLogHandler()

    # Register handlers
    bus.subscribe("user.registered", email_handler)
    bus.subscribe("*", audit_handler)  # Wildcard handler receives all events

    # Publish events
    logging.info("--- Publishing UserRegisteredEvent ---")
    await bus.publish(UserRegisteredEvent(user_id="usr_90", email="alice@example.com"))

    logging.info("\n--- Publishing OrderPlacedEvent ---")
    await bus.publish(OrderPlacedEvent(order_id="ord_300", amount=249.99))


if __name__ == "__main__":
    asyncio.run(main_protocol())