from dataclasses import dataclass
from exc.response_exc import UnprocessableEntity
from exc.request_exc import NotFound, IncorrectHTTPMethod, MethodNotAllowed
from http import HTTPStatus


_HANDLED_EXC = {
    IncorrectHTTPMethod: HTTPStatus.BAD_REQUEST,
    NotFound: HTTPStatus.NOT_FOUND,
    MethodNotAllowed: HTTPStatus.METHOD_NOT_ALLOWED,
    UnprocessableEntity: HTTPStatus.UNPROCESSABLE_ENTITY,
}


@dataclass
class ExceptionResult:
    status: int
    msg: str

    @classmethod
    def from_exc(cls, e: Exception, default_msg: str = 'Server broke') -> "ExceptionResult":
        if status := _HANDLED_EXC.get(type(e)):
            return cls(status=status, msg=str(e))
        else:
            return cls(status=HTTPStatus.INTERNAL_SERVER_ERROR, msg=default_msg)
