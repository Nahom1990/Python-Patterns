import asyncio
import logging
import random
from typing import Awaitable, Callable, Protocol, Sequence, Type, TypeVar, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

T = TypeVar("T")

# 1. STRUCTURAL CONTRACT (PROTOCOL)
class BackoffStrategy(Protocol):
    def calculate_delay(self, attempt: int) -> float: ...


# 2. EXPONENTIAL BACKOFF WITH FULL JITTER STRATEGY
class ExponentialBackoffWithJitter:
    def __init__(self, base_delay: float = 0.1, max_delay: float = 5.0, factor: float = 2.0) -> None:
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.factor = factor

    def calculate_delay(self, attempt: int) -> float:
        # Calculate raw exponential backoff
        calculated = self.base_delay * (self.factor ** attempt)
        capped = min(calculated, self.max_delay)
        # Apply Full Jitter: pick a random value between 0 and the capped delay
        return random.uniform(0, capped)


# 3. REUSABLE RETRY POLICY ENGINE
class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        backoff_strategy: BackoffStrategy = ExponentialBackoffWithJitter(),
        retryable_exceptions: Sequence[Type[Exception]] = (Exception,),
    ) -> None:
        self.max_attempts = max_attempts
        self.backoff_strategy = backoff_strategy
        self.retryable_exceptions = tuple(retryable_exceptions)

    async def execute(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        last_exception: Exception | None = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                logging.info(f"[RetryPolicy] Execution attempt {attempt}/{self.max_attempts}")
                return await func(*args, **kwargs)
            except self.retryable_exceptions as exc:
                last_exception = exc
                if attempt == self.max_attempts:
                    logging.error(f"[RetryPolicy] Max attempts reached. Terminating retry policy.")
                    raise exc

                delay = self.backoff_strategy.calculate_delay(attempt)
                logging.warning(
                    f"[RetryPolicy] Caught transient error: '{exc}'. "
                    f"Retrying in {delay:.3f}s (Attempt {attempt}/{self.max_attempts})..."
                )
                await asyncio.sleep(delay)

        assert last_exception is not None
        raise last_exception


# --- DEMO SERVICE ---
attempt_counter = 0

async def unstable_payment_gateway() -> str:
    global attempt_counter
    attempt_counter += 1
    if attempt_counter < 3:
        raise ConnectionResetError("Gateway temporarily unreachable")
    return "Payment Processed Successfully"


# --- RUNNER ---
async def main_protocol() -> None:
    policy = RetryPolicy(
        max_attempts=4,
        backoff_strategy=ExponentialBackoffWithJitter(base_delay=0.1, max_delay=1.0),
        retryable_exceptions=(ConnectionResetError, TimeoutError),
    )

    result = await policy.execute(unstable_payment_gateway)
    logging.info(f"Final Execution Result: '{result}'")


if __name__ == "__main__":
    asyncio.run(main_protocol())