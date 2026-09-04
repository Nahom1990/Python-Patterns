import asyncio
import logging
from dataclasses import dataclass
from typing import Callable, Awaitable, AsyncGenerator, TypeVar
import uuid

T = TypeVar("T")

@dataclass(frozen=True)
class EventPayload:
    id: str
    data: str

# 1. PURE HIGHER-ORDER WORKER CLOSURE
def make_worker(
    worker_id: int,
    processor: Callable[[EventPayload], Awaitable[None]]
) -> Callable[[asyncio.Queue[EventPayload | None]], Awaitable[None]]:
    """Higher-order function returning an async worker closure."""
    
    async def worker_loop(queue: asyncio.Queue[EventPayload | None]) -> None:
        logging.info(f"[FunctionalWorker-{worker_id}] Ready.")
        while True:
            item = await queue.get()
            
            # None acts as the functional stream termination signal
            if item is None:
                queue.task_done()
                logging.info(f"[FunctionalWorker-{worker_id}] Exiting.")
                break

            try:
                await processor(item)
            except Exception as err:
                logging.error(f"[FunctionalWorker-{worker_id}] Error processing {item.id}: {err}")
            finally:
                queue.task_done()

    return worker_loop


# 2. ASYNC GENERATOR PRODUCER (STREAMING SOURCE)
async def event_stream(total: int) -> AsyncGenerator[EventPayload, None]:
    for i in range(total):
        await asyncio.sleep(0.05)
        yield EventPayload(id=str(uuid.uuid4())[:6], data=f"Payload-{i}")


# 3. PURE PIPELINE RUNNER WITH BACKPRESSURE
async def run_functional_pipeline(
    stream: AsyncGenerator[EventPayload, None],
    processor_fn: Callable[[EventPayload], Awaitable[None]],
    concurrency: int,
    max_queue_size: int
) -> None:
    queue: asyncio.Queue[EventPayload | None] = asyncio.Queue(maxsize=max_queue_size)

    # Spawn workers using higher-order closures
    workers = [
        asyncio.create_task(make_worker(i, processor_fn)(queue))
        for i in range(concurrency)
    ]

    # Stream items from async generator into bounded queue (Enforces Backpressure)
    async for event in stream:
        if queue.full():
            logging.warning(f"[Functional Backpressure] Queue full ({queue.qsize()}/{max_queue_size}). Suspending producer stream.")
        await queue.put(event)

    # Inject termination sentinels for workers
    for _ in range(concurrency):
        await queue.put(None)

    # Wait for completion
    await queue.join()
    await asyncio.gather(*workers)
    logging.info("Functional pipeline processing complete.")


# --- USAGE DEMONSTRATION ---
async def process_event(event: EventPayload) -> None:
    logging.info(f"--> Processing {event.id}: {event.data}")
    await asyncio.sleep(0.4)

async def main_functional() -> None:
    await run_functional_pipeline(
        stream=event_stream(total=8),
        processor_fn=process_event,
        concurrency=3,
        max_queue_size=2  # Tight queue bound to demonstrate backpressure quickly
    )

if __name__ == "__main__":
    asyncio.run(main_functional())