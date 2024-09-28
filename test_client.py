import json

import websockets
import asyncio


async def hello():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        await websocket.send(
            json.dumps({"message_type": "CLIENT_ENTER", "client_type": "unity"})
        )
        msg = await websocket.recv()


if __name__ == "__main__":
    asyncio.run(hello())
