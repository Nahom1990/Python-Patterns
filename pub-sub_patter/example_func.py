import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List
import uuid

# 1. IMMUTABLE EVENT MODEL
@dataclass(frozen=True)
class Event:
    topic: str
    payload: Dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

# Type alias for a subscriber function
EventHandler = Callable[[Event], Awaitable[None]]


# 2. FUNCTIONAL PUB-SUB ENGINE (HIGHER-ORDER CLOSURE)
def create_pubsub_engine():
    """Returns a tuple of functions (publish, subscribe, unsubscribe) sharing a topic registry."""
    registry: Dict[str, List[EventHandler]] = {}

    def subscribe(topic: str, handler: EventHandler) -> Callable[[], None]:
        """Subscribes a handler function and returns an unsubscribe function (cleanup closure)."""
        if topic not in registry:
            registry[topic] = []
        registry[topic].append(handler)
        
        # Return a zero-argument unsubscribe function
        def unsubscribe() -> None:
            if topic in registry and handler in registry[topic]:
                registry[topic].remove(handler)
                
        return unsubscribe

    async def publish(event: Event) -> None:
        handlers = registry.get(event.topic, [])
        if not handlers:
            return

        # Execute all handlers for this topic concurrently
        async def safe_execute(h: EventHandler) -> None:
            try:
                await h(event)
            except Exception as err:
                logging.error(f"Handler error on event {event.id}: {err}")

        await asyncio.gather(*(safe_execute(h) for h in handlers))

    return publish, subscribe


# 3. PURE HANDLER FUNCTIONS (SUBSCRIBERS)

async def log_audit(event: Event) -> None:
    logging.info(f"[FunctionalAudit] Recorded {event.topic} event (ID: {event.id})")
    await asyncio.sleep(0.05)


def make_analytics_collector(source_id: str) -> EventHandler:
    """Higher-order function returning a stateful subscriber handler."""
    count = 0

    async def analytics_handler(event: Event) -> None:
        nonlocal count
        count += 1
        logging.info(
            f"[Analytics - {source_id}] Processed event #{count} on '{event.topic}'"
        )
        await asyncio.sleep(0.1)

    return analytics_handler


# 4. RUNNER
async def main_functional() -> None:
    publish, subscribe = create_pubsub_engine()

    # Create handler instances
    analytics_handler = make_analytics_collector("Cluster-Alpha")

    # Subscribe handlers and keep unsubscribe handles
    unsub_audit = subscribe("payment.processed", log_audit)
    unsub_analytics = subscribe("payment.processed", analytics_handler)

    # Publish
    logging.info("--- Publishing Payment Event ---")
    await publish(
        Event(topic="payment.processed", payload={"amount": 49.99, "currency": "USD"})
    )

    # Dynamic Unsubscribe
    unsub_analytics()
    logging.info("\n--- Unsubscribed Analytics. Publishing Second Event ---")

    # Only log_audit will execute here
    await publish(
        Event(topic="payment.processed", payload={"amount": 12.00, "currency": "USD"})
    )

if __name__ == "__main__":
    asyncio.run(main_functional())