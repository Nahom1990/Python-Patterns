import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, TypeVar
import uuid

# 1. IMMUTABLE EVENT MODEL
@dataclass(frozen=True)
class Event:
    name: str
    payload: Dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:6])

HandlerFn = Callable[[Event], Awaitable[None]]
Middleware = Callable[[HandlerFn], HandlerFn]


# 2. FUNCTIONAL MIDDLEWARES (HIGHER-ORDER DECORATORS)

def logging_middleware(next_handler: HandlerFn) -> HandlerFn:
    """Logs event execution time and payload."""
    async def wrapper(event: Event) -> None:
        logging.info(f"[Middleware:Log] BEFORE handling '{event.name}' ({event.id})")
        await next_handler(event)
        logging.info(f"[Middleware:Log] AFTER handling '{event.name}' ({event.id})")
        
    return wrapper


def recovery_middleware(next_handler: HandlerFn) -> HandlerFn:
    """Protects the pipeline by catching unhandled exceptions."""
    async def wrapper(event: Event) -> None:
        try:
            await next_handler(event)
        except Exception as err:
            logging.error(f"[Middleware:PanicRecovery] Caught exception in '{event.name}': {err}")

    return wrapper


# 3. FUNCTIONAL EVENT BUS ENGINE

def create_event_bus(*middlewares: Middleware):
    """Returns a functional event bus tuple: (publish, subscribe)."""
    routes: Dict[str, List[HandlerFn]] = {}

    def subscribe(event_name: str, handler: HandlerFn) -> None:
        # Wrap the raw handler function through all configured middlewares
        chain = handler
        for mw in reversed(middlewares):
            chain = mw(chain)

        if event_name not in routes:
            routes[event_name] = []
        routes[event_name].append(chain)

    async def publish(event: Event) -> None:
        handlers = routes.get(event.name, [])
        if not handlers:
            return

        # Fire all middleware-wrapped handlers concurrently
        await asyncio.gather(*(h(event) for h in handlers))

    return publish, subscribe


# 4. HANDLER FUNCTIONS

async def send_welcome_sms(event: Event) -> None:
    phone = event.payload.get("phone")
    logging.info(f"--> Sending SMS to {phone}")
    await asyncio.sleep(0.05)


async def failing_analytics_handler(event: Event) -> None:
    logging.info("--> Running analytics calculation...")
    raise ValueError("Analytics engine offline!")


# --- RUNNER ---
async def main_functional() -> None:
    # Build bus with logging and panic recovery middleware pipeline
    publish, subscribe = create_event_bus(logging_middleware, recovery_middleware)

    # Wire handlers
    subscribe("user.signup", send_welcome_sms)
    subscribe("user.signup", failing_analytics_handler)

    # Publish
    logging.info("--- Publishing Event ---")
    await publish(
        Event(name="user.signup", payload={"phone": "+15550199", "user_id": "usr_42"})
    )


if __name__ == "__main__":
    asyncio.run(main_functional())