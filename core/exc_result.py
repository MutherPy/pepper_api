from dataclasses import dataclass
from exc.request_exc import NotFound, IncorrectHTTPMethod, MethodNotAllowed, UnprocessableEntity
from http import HTTPStatus
import traceback


_HANDLED_EXC = {
    IncorrectHTTPMethod: HTTPStatus.BAD_REQUEST,
    NotFound: HTTPStatus.NOT_FOUND,
    MethodNotAllowed: HTTPStatus.METHOD_NOT_ALLOWED,
    UnprocessableEntity: HTTPStatus.UNPROCESSABLE_ENTITY,
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
