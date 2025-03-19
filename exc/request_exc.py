
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


class UnprocessableEntity(Exception):
    pass


class AuthAccessDenied(Exception):
    def __init__(self):
        msg = f'Unauthenticated access denied'
        super().__init__(msg)


class PermAccessDenied(Exception):
    def __init__(self):
        msg = f'Unauthorized access denied'
        super().__init__(msg)


class QueryParamExpected(Exception):
    def __init__(self, q_name):
        msg = f'Expected query parameter: {q_name}'
        super().__init__(msg)
