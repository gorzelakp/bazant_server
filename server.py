import asyncio

import websockets
from websockets import broadcast

WEBSOCKETS = set()


async def handle_websocket(websocket, _):
    if websocket not in WEBSOCKETS:
        WEBSOCKETS.add(websocket)

    try:
        await websocket.send("Device connected to bazant_server!")
        async for msg in websocket:
            broadcast(WEBSOCKETS, msg)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        WEBSOCKETS.remove(websocket)

    # try:
    #     data = json.loads(message)
    # except json.JSONDecodeError:
    #     print("Not supported message")
    #     await websocket.send(json.dumps({"message": "Message not supported"}))


async def main():
    async with websockets.serve(
		handle_websocket,
		host="",
		port=8001,
	):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())