UNITY_CLIENTS = set()
WEB_CLIENTS = set()


class Client:
    def __init__(self, client_id, client_type, websocket):
        self.client_id = client_id
        self.client_type = client_type
        self.websocket = websocket
