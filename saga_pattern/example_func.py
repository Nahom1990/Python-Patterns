import asyncio
import logging
from dataclasses import dataclass
from typing import Awaitable, Callable, Dict, List, Tuple, Any

# Type definitions for pure functions
StepFn = Callable[[Dict[str, Any]], Awaitable[bool]]
CompensateFn = Callable[[Dict[str, Any]], Awaitable[None]]
SagaStepTuple = Tuple[str, StepFn, CompensateFn]


# 1. PURE STEP & COMPENSATION FACTORIES (CLOSURES)

def make_inventory_step():
    async def execute(ctx: Dict[str, Any]) -> bool:
        logging.info(f"[FunctionalInventory] Reserving item {ctx['item_id']}")
        ctx["stock_locked"] = True
        return True

    async def compensate(ctx: Dict[str, Any]) -> None:
        if ctx.get("stock_locked"):
            logging.info(f"[FunctionalInventory] UN-RESERVING item {ctx['item_id']}")

    return "InventoryStep", execute, compensate


def make_payment_step(should_fail: bool = False):
    async def execute(ctx: Dict[str, Any]) -> bool:
        logging.info(f"[FunctionalPayment] Processing payment of ${ctx['amount']}")
        if should_fail:
            logging.error("[FunctionalPayment] Payment Declined!")
            return False
        ctx["paid"] = True
        return True

    async def compensate(ctx: Dict[str, Any]) -> None:
        if ctx.get("paid"):
            logging.info(f"[FunctionalPayment] ISSUING REFUND for ${ctx['amount']}")

    return "PaymentStep", execute, compensate


# 2. FUNCTIONAL SAGA RUNNER ENGINE

async def run_saga_pipeline(steps: List[SagaStepTuple], context: Dict[str, Any]) -> bool:
    """Higher-order function executing steps sequentially and rolling back on failure."""
    completed_steps: List[SagaStepTuple] = []

    for name, execute_fn, compensate_fn in steps:
        logging.info(f"[SagaEngine] Executing: {name}")
        success = await execute_fn(context)

        if success:
            completed_steps.append((name, execute_fn, compensate_fn))
        else:
            logging.warning(f"[SagaEngine] Step '{name}' FAILED. Initiating Compensation...")
            
            # Rollback completed steps in reverse
            for comp_name, _, rollback_fn in reversed(completed_steps):
                logging.info(f"[SagaEngine] Rolling back: {comp_name}")
                await rollback_fn(context)
                
            return False

    return True


# --- RUNNER ---
async def main_functional() -> None:
    context = {"item_id": "laptop_42", "amount": 1200.00}

    saga_steps = [
        make_inventory_step(),
        make_payment_step(should_fail=True)  # Will trigger compensation
    ]

    logging.info("--- Executing Functional Saga ---")
    await run_saga_pipeline(saga_steps, context)


if __name__ == "__main__":
    asyncio.run(main_functional())