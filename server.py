import asyncio
import json
import logging
import websockets

from service import handle_client_enter, handle_client_exit, handle_client_update

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MESSAGE_CLIENT_ENTER = "CLIENT_ENTER"
MESSAGE_CLIENT_UPDATE = "CLIENT_UPDATE"


async def route_message(msg, websocket):
    msg_handler = {
        MESSAGE_CLIENT_ENTER: handle_client_enter,
        MESSAGE_CLIENT_UPDATE: handle_client_update,
    }
    if (msg_type := msg["message_type"]) in msg_handler:
        await msg_handler[msg_type](msg, websocket)
    else:
        await websocket.send(f"Message type not recognized -> {msg}")


async def websocket_handler(websocket, _):
    try:
        await websocket.send("Client connected to bazant_server!")
        logger.info("Client connected to bazant_server!")
        async for msg in websocket:
            msg_data = json.loads(msg)
            await route_message(msg_data, websocket)
    finally:
        client = await handle_client_exit(websocket)
        logger.info(f"Client {client.client_id} left the server!")


async def main():
    async with websockets.serve(
        websocket_handler,
        host="",
        port=8001,
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
