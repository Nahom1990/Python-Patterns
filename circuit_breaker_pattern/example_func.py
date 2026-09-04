import asyncio
import logging
import time
from typing import Awaitable, Callable, Optional, TypeVar, ParamSpec

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

P = ParamSpec("P")
R = TypeVar("R")

# 1. HIGHER-ORDER DECORATOR FACTORY WITH CLOSURE STATE
def circuit_breaker(
    failure_threshold: int = 2,
    recovery_time: float = 1.0,
    fallback: Optional[Callable[..., Awaitable[R]]] = None
):
    """Functional Async Decorator enclosing state in a lexical closure."""
    state = "CLOSED"
    failure_count = 0
    last_state_change = time.monotonic()

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal state, failure_count, last_state_change

            # Evaluate transition to HALF-OPEN
            if state == "OPEN":
                if time.monotonic() - last_state_change >= recovery_time:
                    logging.info("[FunctionalCircuit] Entering HALF-OPEN probe state.")
                    state = "HALF-OPEN"
                else:
                    logging.warning("[FunctionalCircuit] Circuit OPEN - Fast failing.")
                    if fallback:
                        return await fallback(*args, **kwargs)
                    raise RuntimeError("Circuit is OPEN")

            try:
                result = await func(*args, **kwargs)
            except Exception as err:
                failure_count += 1
                logging.error(f"[FunctionalCircuit] Error recorded ({failure_count}/{failure_threshold})")
                
                if state == "HALF-OPEN" or failure_count >= failure_threshold:
                    logging.error("[FunctionalCircuit] Trip threshold reached! Circuit is now OPEN.")
                    state = "OPEN"
                    last_state_change = time.monotonic()

                if fallback:
                    return await fallback(*args, **kwargs)
                raise err
            else:
                if state == "HALF-OPEN":
                    logging.info("[FunctionalCircuit] Probe call succeeded! Resetting to CLOSED.")
                    state = "CLOSED"
                    failure_count = 0
                elif state == "CLOSED":
                    failure_count = 0
                return result

        return wrapper
    return decorator


# 2. DECORATED SERVICE WITH FALLBACK HANDLER

async def fetch_user_fallback(user_id: str) -> dict[str, str]:
    """Graceful degradation fallback returning cached/default payload."""
    logging.info("[Fallback] Returning cached fallback user profile.")
    return {"user_id": user_id, "name": "Cached User", "status": "DEGRADED_MODE"}


@circuit_breaker(failure_threshold=2, recovery_time=0.5, fallback=fetch_user_fallback)
async def fetch_user_from_db(user_id: str) -> dict[str, str]:
    logging.info(f"Querying database for user {user_id}...")
    raise TimeoutError("Database query timed out!")


# --- RUNNER ---
async def main_functional() -> None:
    logging.info("--- Execution 1 (Failure 1 - Fallback Triggered) ---")
    res1 = await fetch_user_from_db("usr_100")
    print(f"Result: {res1}\n")

    logging.info("--- Execution 2 (Failure 2 - Circuit Trips OPEN) ---")
    res2 = await fetch_user_from_db("usr_100")
    print(f"Result: {res2}\n")

    logging.info("--- Execution 3 (Circuit OPEN - Immediate Fast Fail Fallback) ---")
    res3 = await fetch_user_from_db("usr_100")
    print(f"Result: {res3}\n")


if __name__ == "__main__":
    asyncio.run(main_functional())