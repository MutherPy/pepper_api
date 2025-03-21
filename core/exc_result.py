from dataclasses import dataclass

from bases.exc_results import BaseExceptionResult
from exc import request_exc, runtime_exc
from http import HTTPStatus
from websockets.frames import CloseCode
import traceback


_HANDLED_EXC = {
    request_exc.IncorrectHTTPMethod: HTTPStatus.BAD_REQUEST,
    request_exc.NotFound: HTTPStatus.NOT_FOUND,
    request_exc.MethodNotAllowed: HTTPStatus.METHOD_NOT_ALLOWED,
    request_exc.UnprocessableEntity: HTTPStatus.UNPROCESSABLE_ENTITY,
    request_exc.PermAccessDenied: HTTPStatus.FORBIDDEN,
    request_exc.AuthAccessDenied: HTTPStatus.UNAUTHORIZED,
    request_exc.QueryParamExpected: HTTPStatus.BAD_REQUEST,
    runtime_exc.WrongRouting: HTTPStatus.INTERNAL_SERVER_ERROR
}

_HANDLED_WS_EXC = {
    request_exc.NotFound: CloseCode.GOING_AWAY,
    request_exc.PermAccessDenied: CloseCode.POLICY_VIOLATION,
    request_exc.AuthAccessDenied: CloseCode.POLICY_VIOLATION,
    runtime_exc.WrongRouting: CloseCode.INTERNAL_ERROR
}

# TODO potentially sensitive info returns to client. Mb solve using "DEBUG" mode

@dataclass
class ExceptionResult(BaseExceptionResult):
    status: int
    body: str

    @classmethod
    def from_exc(cls, e: Exception) -> "ExceptionResult":
        if status := _HANDLED_EXC.get(type(e)):
            print(traceback.print_tb(e.__traceback__))
            return cls(status=status, body=str(e))
        else:
            print(traceback.print_tb(e.__traceback__))
            return cls(status=HTTPStatus.INTERNAL_SERVER_ERROR, body='Server broke')


@dataclass
class WSExceptionResult(BaseExceptionResult):
    code: int
    reason: str

    @classmethod
    def from_exc(cls, e: Exception) -> "WSExceptionResult":
        if code := _HANDLED_WS_EXC.get(type(e)):
            print(traceback.print_tb(e.__traceback__))
            return cls(code=code, reason=str(e))
        else:
            print(traceback.print_tb(e.__traceback__))
            return cls(code=CloseCode.INTERNAL_ERROR, reason=str(e))

