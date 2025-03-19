from dataclasses import dataclass
from exc import request_exc
from http import HTTPStatus
import traceback


_HANDLED_EXC = {
    request_exc.IncorrectHTTPMethod: HTTPStatus.BAD_REQUEST,
    request_exc.NotFound: HTTPStatus.NOT_FOUND,
    request_exc.MethodNotAllowed: HTTPStatus.METHOD_NOT_ALLOWED,
    request_exc.UnprocessableEntity: HTTPStatus.UNPROCESSABLE_ENTITY,
    request_exc.PermAccessDenied: HTTPStatus.FORBIDDEN,
    request_exc.AuthAccessDenied: HTTPStatus.UNAUTHORIZED,
}


@dataclass
class ExceptionResult:
    status: int
    body: str

    @classmethod
    def from_exc(cls, e: Exception, default_msg: str = 'Server broke') -> "ExceptionResult":
        if status := _HANDLED_EXC.get(type(e)):
            print(traceback.print_tb(e.__traceback__))
            return cls(status=status, body=str(e))
        else:
            print(traceback.print_tb(e.__traceback__))
            return cls(status=HTTPStatus.INTERNAL_SERVER_ERROR, body=default_msg)
