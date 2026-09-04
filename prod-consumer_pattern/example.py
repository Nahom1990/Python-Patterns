"""Producer
   │
   │ creates work
   ▼
┌────────────────┐
│     Queue      │
└────────────────┘
   │
   │ takes work
   ▼
Consumer


Producer

Creates work:

queue.put(work)
Queue

Buffers work:

[work1, work2, work3, work4]
Consumer

Takes work:

work = queue.get()
process(work)"""

import asyncio
import logging
import signal
from dataclasses import dataclass, field
from typing import Protocol, TypeVar, Generic, Optional
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s: %(message)s"
)

T = TypeVar("T")

# 1. STRUCTURAL CONTRACT (PROTOCOL)
class AsyncQueue(Protocol[T]):
    """Decouples queue consumers/producers from asyncio.Queue implementation."""
    async def put(self, item: T) -> None: ...
    async def get(self) -> T: ...
    def task_done(self) -> None: ...
    def qsize(self) -> int: ...

@dataclass(frozen=True)
class WorkItem:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    payload: str = ""

# Sentinel object used to signal workers to shut down gracefully
SHUTDOWN_SENTINEL = WorkItem(id="SHUTDOWN", payload="STOP")


# 2. WORKER IMPLEMENTATION
class ConsumerWorker:
    def __init__(self, worker_id: int, queue: AsyncQueue[WorkItem]) -> None:
        self.worker_id = worker_id
        self.queue = queue

    async def run(self, shutdown_event: asyncio.Event) -> None:
        logging.info(f"Worker-{self.worker_id} started.")
        while not shutdown_event.is_set():
            try:
                # Timeout allows checking the shutdown_event periodically
                item = await asyncio.wait_for(self.queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue

            if item is SHUTDOWN_SENTINEL:
                self.queue.task_done()
                logging.info(f"Worker-{self.worker_id} received shutdown signal.")
                break

            try:
                await self._process(item)
            except Exception as exc:
                logging.error(f"Worker-{self.worker_id} failed item {item.id}: {exc}")
            finally:
                self.queue.task_done()

        logging.info(f"Worker-{self.worker_id} stopped.")

    async def _process(self, item: WorkItem) -> None:
        logging.info(f"Worker-{self.worker_id} processing {item.id} ({item.payload})")
        await asyncio.sleep(0.5)  # Simulate workload


# 3. PRODUCER WITH BACKPRESSURE
async def producer(
    queue: AsyncQueue[WorkItem], 
    total_items: int, 
    shutdown_event: asyncio.Event
) -> None:
    for i in range(total_items):
        if shutdown_event.is_set():
            logging.warning("Producer stopping early due to shutdown signal.")
            break

        item = WorkItem(payload=f"DataPacket-{i}")
        
        # BACKPRESSURE: queue.put() will suspend execution if maxsize is reached
        if queue.qsize() >= 3:
            logging.warning(f"[Backpressure Active] Queue full ({queue.qsize()} items). Producer pausing...")
        
        await queue.put(item)
        logging.info(f"Produced {item.id} (Queue size: {queue.qsize()})")
        await asyncio.sleep(0.1)


# 4. ORCHESTRATOR / PIPELINE RUNNER
async def main_protocol() -> None:
    # Bounded queue enforces Backpressure (maxsize=3)
    queue: asyncio.Queue[WorkItem] = asyncio.Queue(maxsize=3)
    shutdown_event = asyncio.Event()
    num_workers = 3

    # Setup workers
    workers = [ConsumerWorker(i, queue) for i in range(num_workers)]
    worker_tasks = [
        asyncio.create_task(w.run(shutdown_event), name=f"Worker-{i}")
        for i, w in enumerate(workers)
    ]

    # Handle OS Signals for Graceful Teardown (SIGINT / SIGTERM)
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown_event.set)
        except NotImplementedError:
            pass  # Windows signal handling fallback

    # Run producer
    producer_task = asyncio.create_task(producer(queue, total_items=10, shutdown_event=shutdown_event))
    
    await producer_task
    
    # Send shutdown sentinels to drain workers
    for _ in range(num_workers):
        await queue.put(SHUTDOWN_SENTINEL)

    # Wait for all queued items to be processed
    await queue.join()

    # Cancel workers if any are stuck in wait_for loops
    shutdown_event.set()
    await asyncio.gather(*worker_tasks, return_exceptions=True)
    logging.info("All pipeline tasks completed cleanly.")


if __name__ == "__main__":
    asyncio.run(main_protocol())