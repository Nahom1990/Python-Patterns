import asyncio
import logging
import time
from typing import Awaitable, Callable, Protocol, TypeVar, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

T = TypeVar("T")

class RateLimitExceededError(Exception):
    """Raised when a request violates rate limits."""
    pass


# 1. STRUCTURAL CONTRACT (PROTOCOL)
class RateLimiter(Protocol):
    async def acquire(self, tokens: int = 1) -> bool: ...
    async def decorate(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T: ...


# 2. TOKEN BUCKET IMPLEMENTATION
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float) -> None:
        """
        :param capacity: Max burst capacity (tokens).
        :param refill_rate: Tokens added per second.
        """
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    async def acquire(self, tokens: int = 1) -> bool:
        async with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    async def decorate(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        if not await self.acquire():
            logging.warning("[RateLimiter] Rate limit exceeded! Request rejected.")
            raise RateLimitExceededError("Too Many Requests (429)")
        return await func(*args, **kwargs)


# --- DEMO SERVICE ---
async def process_payment(user_id: str, amount: float) -> str:
    logging.info(f"Processing ${amount} for user {user_id}")
    return "SUCCESS"


# --- RUNNER ---
async def main_protocol() -> None:
    # 2 tokens max capacity, refills at 1 token per second
    limiter: RateLimiter = TokenBucketRateLimiter(capacity=2, refill_rate=1.0)

    # 1. Burst of 2 calls (Should both succeed instantly)
    logging.info("--- Sending Burst of 2 Requests ---")
    await limiter.decorate(process_payment, "usr_1", 50.0)
    await limiter.decorate(process_payment, "usr_1", 30.0)

    # 2. Immediate 3rd call (Should fail fast)
    logging.info("--- Attempting 3rd Request Immediately ---")
    try:
        await limiter.decorate(process_payment, "usr_1", 10.0)
    except RateLimitExceededError as err:
        logging.error(f"Caught Expected Limit: {err}")

    # 3. Wait 1 second to refill 1 token
    logging.info("Sleeping 1.0s to refill tokens...")
    await asyncio.sleep(1.0)

    # 4. Attempt call again (Should succeed)
    res = await limiter.decorate(process_payment, "usr_1", 20.0)
    logging.info(f"Post-refill execution result: {res}")


if __name__ == "__main__":
    asyncio.run(main_protocol())