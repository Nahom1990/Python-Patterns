import asyncio
import logging
import random
from typing import Awaitable, Callable, ParamSpec, Sequence, Type, TypeVar,Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

P = ParamSpec("P")
R = TypeVar("R")

# 1. HIGHER-ORDER DECORATOR WITH CLOSURE
def retry(
    max_attempts: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 2.0,
    retryable_exceptions: Sequence[Type[Exception]] = (Exception,),
):
    """Functional Async Decorator applying exponential backoff with full jitter."""
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except tuple(retryable_exceptions) as exc:
                    if attempt == max_attempts:
                        logging.error(f"[FunctionalRetry] Function {func.__name__} failed on final attempt.")
                        raise exc

                    # Calculate exponential delay with full jitter
                    delay = random.uniform(0, min(base_delay * (2 ** (attempt - 1)), max_delay))
                    logging.warning(
                        f"[FunctionalRetry] {func.__name__} failed with {exc.__class__.__name__}: '{exc}'. "
                        f"Retrying in {delay:.3f}s (Attempt {attempt}/{max_attempts})"
                    )
                    await asyncio.sleep(delay)

            raise RuntimeError("Unreachable code path in retry wrapper")

        return wrapper
    return decorator


# 2. DECORATED SERVICE WITH SPECIFIC TRANSIENT FILTERING

call_count = 0

@retry(
    max_attempts=3,
    base_delay=0.05,
    retryable_exceptions=(TimeoutError, ConnectionError)
)
async def fetch_remote_data(endpoint: str) -> dict[str, Any]:
    global call_count
    call_count += 1
    logging.info(f"Connecting to {endpoint}...")
    
    if call_count < 3:
        raise TimeoutError("Network socket timed out")
    
    return {"status": 200, "data": "payload"}


# --- RUNNER ---
async def main_functional() -> None:
    data = await fetch_remote_data("https://api.internal/v1/metrics")
    logging.info(f"Received Payload: {data}")


if __name__ == "__main__":
    asyncio.run(main_functional())