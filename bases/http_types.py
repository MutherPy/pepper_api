from collections import namedtuple


RequestType = namedtuple(
    'RequestType', ('HTTP', )
)("http")

ReceiveEventType = namedtuple(
    'ReceiveEventType', ('START', 'DISCONNECT')
)("http.request", "http.disconnect")

SendEventTypes = namedtuple(
    'SendEventTypes', ('START', 'DISCONNECT')
)("http.response.start", "http.response.body")
