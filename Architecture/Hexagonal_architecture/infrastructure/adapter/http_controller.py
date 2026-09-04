# infrastructure/adapters/http_controller.py
from fastapi import APIRouter, HTTPException, Depends
from domain.ports import CheckoutUseCasePort

router = APIRouter()

# Controller only depends on the Primary Port interface!
@router.post("/orders/{order_id}/checkout")
async def checkout_endpoint(
    order_id: str, 
    use_case: CheckoutUseCasePort = Depends(...)
):
    try:
        order = await use_case.execute(order_id)
        return {"order_id": order.id, "status": order.status.value}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except RuntimeError as err:
        raise HTTPException(status_code=502, detail=str(err))