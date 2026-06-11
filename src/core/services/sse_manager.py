import asyncio


class SSEManager:
    def __init__(self) -> None:
        self.subscribers: list[asyncio.Queue[str]] = []

    def subscribe(
        self,
    ) -> asyncio.Queue[str]:
        queue: asyncio.Queue[str] = asyncio.Queue()

        self.subscribers.append(queue)

        return queue

    def unsubscribe(
        self,
        queue: asyncio.Queue[str],
    ) -> None:
        if queue in self.subscribers:
            self.subscribers.remove(queue)

    async def publish(
        self,
        message: str,
    ) -> None:
        for queue in self.subscribers:
            await queue.put(message)


sse_manager = SSEManager()
