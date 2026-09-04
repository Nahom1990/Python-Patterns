import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol, Optional
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 1. SAGA STEP CONTRACT (PROTOCOL)
class SagaStep(Protocol):
    @property
    def name(self) -> str: ...
    async def execute(self, context: Dict[str, Any]) -> bool: ...
    async def compensate(self, context: Dict[str, Any]) -> None: ...


# 2. CONCRETE SAGA STEPS

class InventoryStep:
    @property
    def name(self) -> str:
        return "ReserveInventory"

    async def execute(self, context: Dict[str, Any]) -> bool:
        logging.info(f"[{self.name}] Reserving stock for item {context['item_id']}...")
        await asyncio.sleep(0.1)
        context["inventory_reserved"] = True
        return True  # Success

    async def compensate(self, context: Dict[str, Any]) -> None:
        if context.get("inventory_reserved"):
            logging.info(f"[{self.name}] COMPENSATING: Releasing stock for item {context['item_id']}.")
            await asyncio.sleep(0.1)


class PaymentStep:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail

    @property
    def name(self) -> str:
        return "ProcessPayment"

    async def execute(self, context: Dict[str, Any]) -> bool:
        logging.info(f"[{self.name}] Charging ${context['amount']} to customer {context['user_id']}...")
        await asyncio.sleep(0.1)
        
        if self.should_fail:
            logging.error(f"[{self.name}] Payment failed due to insufficient funds!")
            return False

        context["payment_processed"] = True
        return True

    async def compensate(self, context: Dict[str, Any]) -> None:
        if context.get("payment_processed"):
            logging.info(f"[{self.name}] COMPENSATING: Refunding ${context['amount']} to {context['user_id']}.")
            await asyncio.sleep(0.1)


class ShippingStep:
    @property
    def name(self) -> str:
        return "CreateShippingLabel"

    async def execute(self, context: Dict[str, Any]) -> bool:
        logging.info(f"[{self.name}] Generating shipping label...")
        await asyncio.sleep(0.1)
        return True

    async def compensate(self, context: Dict[str, Any]) -> None:
        logging.info(f"[{self.name}] COMPENSATING: Canceling shipping label.")


# 3. SAGA ORCHESTRATOR
class SagaOrchestrator:
    def __init__(self, steps: List[SagaStep]) -> None:
        self.steps = steps

    async def execute(self, context: Dict[str, Any]) -> bool:
        executed_steps: List[SagaStep] = []

        for step in self.steps:
            logging.info(f"--> Starting Step: {step.name}")
            success = await step.execute(context)

            if success:
                executed_steps.append(step)
            else:
                logging.warning(f"Step '{step.name}' failed! Initiating compensation sequence...")
                await self._compensate(executed_steps, context)
                return False

        logging.info("Saga completed successfully!")
        return True

    async def _compensate(self, executed_steps: List[SagaStep], context: Dict[str, Any]) -> None:
        # Compensate in REVERSE order of execution
        for step in reversed(executed_steps):
            try:
                await step.compensate(context)
            except Exception as exc:
                logging.critical(f"Compensation step '{step.name}' failed: {exc}")


# --- RUNNER ---
async def main_protocol() -> None:
    context = {"user_id": "usr_77", "item_id": "sku_900", "amount": 199.99}

    # Scenario 1: Failure at payment step
    logging.info("=== TEST 1: Failing Payment Scenario ===")
    failing_saga = SagaOrchestrator([
        InventoryStep(),
        PaymentStep(should_fail=True),
        ShippingStep()
    ])
    await failing_saga.execute(context.copy())


if __name__ == "__main__":
    asyncio.run(main_protocol())