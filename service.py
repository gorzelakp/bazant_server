import json
import uuid

from websockets import broadcast

from models import UNITY_CLIENTS, WEB_CLIENTS, Client
from server import logger


def get_client_by_websocket(websocket):
    for elem in [UNITY_CLIENTS, WEB_CLIENTS]:
        for client in elem:
            if client.websocket is websocket:
                return client
    logger.warning("Client not found!")


async def handle_client_enter(msg, websocket):
    if not (client_type := msg.get("client_type")):
        logger.warning(f"Wrong message, no client_type -> {msg}")
        return
    client = Client(str(uuid.uuid4()), client_type, websocket)
    if client.client_type == "unity":
        UNITY_CLIENTS.add(client)
    else:
        WEB_CLIENTS.add(client)


async def handle_client_update(msg, websocket):
    if client := get_client_by_websocket(websocket):
        msg_data = json.dumps(msg)
        if client.client_type == "unity":
            broadcast([client.websocket for client in WEB_CLIENTS], msg_data)
        else:
            broadcast([client.websocket for client in UNITY_CLIENTS], msg_data)


async def handle_client_exit(websocket):
    for elem in [UNITY_CLIENTS, WEB_CLIENTS]:
        for client in list(elem):
            if client.websocket is websocket:
                elem.remove(client)
                return client
