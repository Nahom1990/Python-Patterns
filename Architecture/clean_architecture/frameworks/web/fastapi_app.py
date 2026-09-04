# frameworks/web/fastapi_app.py
from fastapi import FastAPI, Request, Response
from adapters.controllers.user_controller import UserController

app = FastAPI()

# Injected wiring happens at the outermost infrastructure layer
@app.post("/users/{user_id}/upgrade")
async def upgrade_endpoint(user_id: str, request: Request, response: Response):
    body = await request.json()
    
    # Factory/Container supplies configured controller
    controller: UserController = app.state.container.user_controller()
    
    data, status_code = await controller.handle_upgrade_request(user_id, body)
    response.status_code = status_code
    return data