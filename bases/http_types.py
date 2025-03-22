from typing import NamedTuple, Optional


class _ScopeType(NamedTuple):
    HTTP: str = "http"
    LIFE: str = "lifespan"
    WS: str = "websocket"

    def check_type(self, type_to_check: str) -> Optional[str]:
        type_to_check_l = type_to_check.lower()
        return type_to_check_l if type_to_check in self else None


class _RequestType(NamedTuple):
    COMMON_HTTP: str = "http"
    FILE_HTTP: str = "http_file"
    BIGFILE_HTTP: str = "http_big_file"
    COMMON_WS: str = "ws"


class _HTTPReceiveEventType(NamedTuple):
    START: str = "http.request"
    DISCONNECT: str = "http.disconnect"


class _HTTPSendEventTypes(NamedTuple):
    START: str = "http.response.start"
    BODY: str = "http.response.body"


class _WSReceiveEventTypes(NamedTuple):
    CONNECT = "websocket.connect"
    RECEIVE = "websocket.receive"
    DISCONNECT = "websocket.disconnect"


class _WSSendEventTypes(NamedTuple):
    ACCEPT = "websocket.accept"
    SEND = "websocket.send"
    CLOSE = "websocket.close"


class _ResponseType(NamedTuple):
    HTTP: str = "HTTP"
    STREAM: str = "STREAM"


ScopeType = _ScopeType()
RequestType = _RequestType()
HTTPReceiveEventType = _HTTPReceiveEventType()
HTTPSendEventTypes = _HTTPSendEventTypes()
WSReceiveEventTypes = _WSReceiveEventTypes()
WSSendEventTypes = _WSSendEventTypes()
ResponseType = _ResponseType()
