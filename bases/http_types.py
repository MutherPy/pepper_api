from collections import namedtuple


RequestType = namedtuple(
    'RequestType', ('HTTP', "LIFE", "WS")
)("http", "lifespan", "websocket")

HTTPReceiveEventType = namedtuple(
    'ReceiveEventType', ('START', 'DISCONNECT')
)("http.request", "http.disconnect")

HTTPSendEventTypes = namedtuple(
    'SendEventTypes', ('START', 'BODY')
)("http.response.start", "http.response.body")

WSReceiveEventTypes = namedtuple(
    'WSReceiveEventTypes', ('CONNECT', 'RECEIVE', 'DISCONNECT')
)('websocket.connect', 'websocket.receive', 'websocket.disconnect')

WSSendEventTypes = namedtuple(
    'WSSendEventTypes', ('ACCEPT', 'SEND', 'CLOSE')
)('websocket.accept', 'websocket.send', 'websocket.close')


ResponseType = namedtuple('ResponseType', ('HTTP', 'STREAM'))('HTTP', 'STREAM')
