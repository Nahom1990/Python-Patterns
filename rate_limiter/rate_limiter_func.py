import asyncio
import logging
import time
from typing import Awaitable, Callable, ParamSpec, TypeVar, Optional,Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

P = ParamSpec("P")
R = TypeVar("R")

# 1. HIGHER-ORDER DECORATOR WITH CLOSURE
def rate_limit(capacity: int, refill_rate: float, fallback: Optional[Callable[..., Awaitable[R]]] = None):
    """
    Functional Async Rate Limiter decorator using Token Bucket algorithm.
    """
    tokens = float(capacity)
    last_refill = time.monotonic()
    lock = asyncio.Lock()

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal tokens, last_refill

            async with lock:
                now = time.monotonic()
                elapsed = now - last_refill
                tokens = min(float(capacity), tokens + elapsed * refill_rate)
                last_refill = now

                if tokens >= 1.0:
                    tokens -= 1.0
                    allowed = True
                else:
                    allowed = False

            if allowed:
                return await func(*args, **kwargs)
            else:
                logging.warning(f"[FunctionalRateLimiter] Rate limit exceeded on '{func.__name__}'")
                if fallback:
                    return await fallback(*args, **kwargs)
                raise RuntimeError("429 Too Many Requests")

        return wrapper
    return decorator


# 2. DECORATED SERVICE WITH FALLBACK HANDLER

async def rate_limit_fallback(search_term: str) -> dict[str, Any]:
    return {"status": 429, "error": "Rate limit exceeded. Please wait before searching again."}


@rate_limit(capacity=2, refill_rate=1.0, fallback=rate_limit_fallback)
async def search_catalog(search_term: str) -> dict[str, Any]:
    logging.info(f"Searching catalog for '{search_term}'...")
    return {"status": 200, "results": [f"item_{search_term}"]}


# --- RUNNER ---
async def main_functional() -> None:
    logging.info("--- Request 1 ---")
    print(await search_catalog("python"))

    logging.info("--- Request 2 ---")
    print(await search_catalog("asyncio"))

    logging.info("--- Request 3 (Exceeds Capacity) ---")
    print(await search_catalog("architecture"))


if __name__ == "__main__":
    asyncio.run(main_functional())