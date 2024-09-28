import websockets
import asyncio

async def hello():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        # print(f'Client sent: {name}')
        #
        greeting = await websocket.recv()
        print(f"Client received: {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())