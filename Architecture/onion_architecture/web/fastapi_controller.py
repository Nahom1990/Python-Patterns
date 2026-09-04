
# infrastructure/web/fastapi_controller.py
from fastapi import APIRouter, HTTPException, Depends
from Architecture.onion_architecture.application.service import FulfillOrderApplicationService

router = APIRouter()

@router.post("/inventory/fulfill")
async def fulfill_stock_endpoint(
    sku: str, 
    quantity: int, 
    app_service: FulfillOrderApplicationService = Depends(...)
):
    try:
        result = await app_service.fulfill_item(sku, quantity)
        return {"status": "SUCCESS", "data": result}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))