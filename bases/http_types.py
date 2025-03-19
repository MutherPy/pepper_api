from collections import namedtuple


RequestType = namedtuple(
    'RequestType', ('HTTP', "LIFE")
)("http", "lifespan")

ReceiveEventType = namedtuple(
    'ReceiveEventType', ('START', 'DISCONNECT')
)("http.request", "http.disconnect")

SendEventTypes = namedtuple(
    'SendEventTypes', ('START', 'BODY')
)("http.response.start", "http.response.body")


ResponseType = namedtuple('ResponseType', ('HTTP', 'STREAM'))('HTTP', 'STREAM')
