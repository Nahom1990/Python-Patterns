"""
Observer Pattern: Objects talk to each other directly. 
The subject maintains a list of its observers and invokes their methods directly in memory.

Pub–Sub Pattern: Publishers and subscribers never know each other exist. 
They communicate strictly through an intermediate message broker, bus, or channel.

BSERVER PATTERN (Direct / In-Memory):
[Subject]  ──────(Calls notify() directly)──────>  [Observer A]
           ──────(Calls notify() directly)──────>  [Observer B]


PUB-SUB PATTERN (Decoupled via Broker):
[Publisher A]  ──(Publishes to topic)──>  ┌─────────────┐  ──(Routes)──>  [Subscriber X]
[Publisher B]  ──(Publishes to topic)──>  │ Message Bus │  ──(Routes)──>  [Subscriber Y]
                                          └─────────────┘  ──(Routes)──>  [Subscriber Z]
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Protocol, Dict, List, Set, TypeVar
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 1. DOMAIN EVENTS
@dataclass(frozen=True)
class Event:
    topic: str
    payload: Dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

# 2. STRUCTURAL CONTRACT (PROTOCOL)
class Subscriber(Protocol):
    """Any object with an async 'on_event' method satisfies this interface."""
    async def on_event(self, event: Event) -> None: ...


# 3. CONCRETE SUBSCRIBERS
class AuditLogger:
    def __init__(self, name: str) -> None:
        self.name = name

    async def on_event(self, event: Event) -> None:
        logging.info(f"[{self.name}] Auditing event {event.id} on '{event.topic}'")
        await asyncio.sleep(0.1)


class EmailNotifier:
    def __init__(self, recipient: str) -> None:
        self.recipient = recipient

    async def on_event(self, event: Event) -> None:
        # Simulate processing logic
        user = event.payload.get("user", "Unknown")
        logging.info(f"[EmailNotifier] Sending email to {self.recipient} for {user}")
        await asyncio.sleep(0.2)


# 4. EVENT BUS
class EventBus:
    def __init__(self) -> None:
        # Topic -> Set of Subscribers
        self._subscribers: Dict[str, Set[Subscriber]] = {}

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        if topic not in self._subscribers:
            self._subscribers[topic] = set()
        self._subscribers[topic].add(subscriber)
        logging.info(f"Subscribed {subscriber.__class__.__name__} to topic '{topic}'")

    def unsubscribe(self, topic: str, subscriber: Subscriber) -> None:
        if topic in self._subscribers:
            self._subscribers[topic].discard(subscriber)

    async def publish(self, event: Event) -> None:
        """Dispatches an event concurrently to all subscribers registered to its topic."""
        subscribers = self._subscribers.get(event.topic, set())
        if not subscribers:
            logging.warning(f"No subscribers found for topic '{event.topic}'")
            return

        # Fire notification tasks concurrently across subscribers using gather
        tasks = [
            asyncio.create_task(self._safe_notify(sub, event))
            for sub in subscribers
        ]
        await asyncio.gather(*tasks)

    async def _safe_notify(self, subscriber: Subscriber, event: Event) -> None:
        """Isolates subscriber errors so one failing handler doesn't crash the bus."""
        try:
            await subscriber.on_event(event)
        except Exception as exc:
            logging.error(f"Subscriber {subscriber} failed on event {event.id}: {exc}")


# 5. ORCHESTRATION / MAIN
async def main_protocol() -> None:
    bus = EventBus()

    audit_service = AuditLogger("GlobalAudit")
    email_service = EmailNotifier("admin@example.com")

    # Wire up subscriptions
    bus.subscribe("user.registered", audit_service)
    bus.subscribe("user.registered", email_service)
    bus.subscribe("order.created", audit_service)

    # Publish events
    logging.info("--- Publishing Event 1 ---")
    await bus.publish(
        Event(topic="user.registered", payload={"user": "Alice", "role": "Admin"})
    )

    logging.info("\n--- Publishing Event 2 ---")
    await bus.publish(
        Event(topic="order.created", payload={"order_id": 9901, "amount": 150.00})
    )

if __name__ == "__main__":
    asyncio.run(main_protocol())