from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.core.services.websocket_manager import (
    websocket_manager,
)

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
) -> None:
    await websocket_manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive_text()

            await websocket_manager.send(
                websocket,
                f"Echo: {message}",
            )

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
