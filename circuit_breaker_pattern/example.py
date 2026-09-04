"""
The Circuit Breaker pattern protects system stability and prevents 
catastrophic cascading failures when calling remote services or external 
resources that may be degraded, slow, or offline.

Instead of endlessly hammering a failing dependency (which exhausts 
threads, fills queues, and drags down your entire application), a Circuit 
Breaker wraps the network call and monitors for failures.


                 ┌────────────────────────────────┐
                 │                                │
                 ▼                                │ Success count >= Threshold
           ┌───────────┐   Failure threshold      │
           │   CLOSED  │ ──────────────────────┐  │
           │ (Normal)  │                       │  │
           └───────────┘                       ▼  │
                 ▲                       ┌───────────┐
                 │                       │   OPEN    │
   Success call  │                       │ (Failing) │
                 │                       └───────────┘
                 │                             │
                 │     Sleep window expires    │
                 │   ┌─────────────────────────┘
                 │   │
           ┌───────────┐
           │ HALF-OPEN │
           │ (Testing) │
           └───────────┘
                 │
                 │ Failure on test call
                 └─────────────────────────────► OPEN
                 
CLOSED (Normal Operation): Requests pass through directly. 
    The circuit monitors execution metrics. If the failure rate crosses a specified threshold, 
    the state transitions to OPEN.

OPEN (Failing Fast): Calls fail immediately without even attempting to 
    execute the remote request, throwing a CircuitBreakerOpenError or 
    returning a fallback payload. A timer starts.

HALF-OPEN (Probing Recovery): Once the timer/sleep window expires, 
    the circuit allows a single trial request through. If it succeeds, 
    the circuit resets to CLOSED. If it fails, the circuit drops back to 
    OPEN for another sleep duration.

"""

import asyncio
import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Awaitable, Callable, Protocol, TypeVar

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

T = TypeVar("T")

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenError(Exception):
    """Raised when an operation is blocked because the circuit is OPEN."""
    pass


# 1. STRUCTURAL CONTRACT (PROTOCOL)
class CircuitBreaker(Protocol):
    @property
    def state(self) -> CircuitState: ...
    async def call(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T: ...


# 2. CONCRETE IMPLEMENTATION
class AsyncCircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_time: float = 2.0,
        success_threshold: int = 1,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.success_threshold = success_threshold

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_state_change = time.monotonic()
        self._lock = asyncio.Lock()

    @property
    def state(self) -> CircuitState:
        return self._state

    async def call(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        async with self._lock:
            self._evaluate_state()

            if self._state == CircuitState.OPEN:
                logging.warning("[CircuitBreaker] Request BLOCKED - Circuit is OPEN.")
                raise CircuitBreakerOpenError("Circuit is OPEN. Fast failing request.")

        # Execute the call outside the state lock to prevent blocking concurrent calls
        try:
            result = await func(*args, **kwargs)
        except Exception as exc:
            await self._on_failure()
            raise exc
        else:
            await self._on_success()
            return result

    def _evaluate_state(self) -> None:
        """Transitions state from OPEN to HALF_OPEN when recovery time expires."""
        if self._state == CircuitState.OPEN:
            elapsed = time.monotonic() - self._last_state_change
            if elapsed >= self.recovery_time:
                logging.info("[CircuitBreaker] Recovery window expired. Switching to HALF-OPEN (Probing).")
                self._state = CircuitState.HALF_OPEN
                self._success_count = 0

    async def _on_success(self) -> None:
        async with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.success_threshold:
                    logging.info("[CircuitBreaker] Probe succeeded! Closing circuit.")
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
            elif self._state == CircuitState.CLOSED:
                self._failure_count = 0

    async def _on_failure(self) -> None:
        async with self._lock:
            self._failure_count += 1
            logging.error(f"[CircuitBreaker] Recorded failure ({self._failure_count}/{self.failure_threshold})")

            if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.failure_threshold:
                logging.error("[CircuitBreaker] Failure threshold met or probe failed! Opening circuit.")
                self._state = CircuitState.OPEN
                self._last_state_change = time.monotonic()


# --- DEMO SERVICE CALLS ---
async def flaky_unstable_api(fail: bool = False) -> str:
    if fail:
        raise ConnectionResetError("Remote API call timed out!")
    return "API Response 200 OK"


# --- RUNNER ---
async def main_protocol() -> None:
    breaker: CircuitBreaker = AsyncCircuitBreaker(failure_threshold=2, recovery_time=1.0)

    # 1. Trigger failures to OPEN the circuit
    for i in range(2):
        try:
            await breaker.call(flaky_unstable_api, fail=True)
        except ConnectionResetError:
            pass

    # 2. Next call should immediately throw CircuitBreakerOpenError without attempting the call
    logging.info(f"Current State: {breaker.state}")
    try:
        await breaker.call(flaky_unstable_api, fail=False)
    except CircuitBreakerOpenError as err:
        logging.info(f"Caught expected fast-fail: {err}")

    # 3. Wait for recovery window to elapse
    logging.info("Sleeping to allow recovery time...")
    await asyncio.sleep(1.1)

    # 4. Probe call (HALF-OPEN) succeeds and resets the circuit back to CLOSED
    response = await breaker.call(flaky_unstable_api, fail=False)
    logging.info(f"Probe Result: '{response}' | Circuit State: {breaker.state}")


if __name__ == "__main__":
    asyncio.run(main_protocol())