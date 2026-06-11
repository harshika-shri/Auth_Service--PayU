from collections.abc import AsyncGenerator

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from src.core.services.sse_manager import (
    sse_manager,
)

router = APIRouter(
    prefix="/sse",
    tags=["SSE"],
)


@router.get("/stream")
async def stream() -> EventSourceResponse:
    queue = sse_manager.subscribe()

    async def event_generator() -> AsyncGenerator[dict[str, str], None]:
        try:
            while True:
                message = await queue.get()

                yield {
                    "event": "message",
                    "data": message,
                }

        finally:
            sse_manager.unsubscribe(queue)

    return EventSourceResponse(
        event_generator(),
    )


@router.post("/publish")
async def publish() -> dict[str, str]:
    await sse_manager.publish("Hello from SSE")

    return {"status": "published"}
