
class IncorrectHTTPMethod(Exception):
    pass


class NotFound(Exception):
    def __init__(self, path: str):
        msg = f'{path} not found.'
        super().__init__(msg)


class MethodNotAllowed(Exception):
    def __init__(self, method: str):
        msg = f'{method.upper()} method is not allowed.'
        super().__init__(msg)
