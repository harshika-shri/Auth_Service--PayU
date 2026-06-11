from __future__ import annotations

import asyncio


async def main() -> None:
    try:
        import websockets
    except ImportError as exc:
        raise SystemExit(
            "Install the 'websockets' package to run this example."
        ) from exc

    url = "ws://127.0.0.1:8000/websocket/sample"

    async with websockets.connect(url) as websocket:
        print(await websocket.recv())
        await websocket.send("hello")
        print(await websocket.recv())
        await websocket.send("custom message")
        print(await websocket.recv())


if __name__ == "__main__":
    asyncio.run(main())
