
class IncorrectRegistering(Exception):
    def __init__(self, cls: object):
        msg = f'{cls.__name__} already registered.'
        super().__init__(msg)


class MissedRegistering(Exception):
    def __init__(self, cls_type: str):
        msg = f'"{cls_type}" missed in register table.'
        super().__init__(msg)


class IncorrectInheritance(Exception):
    def __init__(self, cls: object, needed: object):
        msg = f'{cls.__name__} class must be derived from {needed.__name__}'
        super().__init__(msg)


class ServiceError(Exception):
    def __init__(self, *args):
        if not args:
            msg = "Incorrect processing"
        else:
            msg = f"Incorrect processing: {', '.join(args)}"
        super().__init__(msg)


class EmptyArgumentAnnotation(Exception):
    def __init__(self, arg):
        msg = f"Not annotated controller argument: {arg}"
        super().__init__(msg)


class TooMuchUrlParams(Exception):
    def __init__(self, arg):
        msg = f"Too much parameters for controller: {', '.join(arg)}"
        super().__init__(msg)


class NotEnoughUrlParams(Exception):
    def __init__(self, arg):
        msg = f"Not enough parameters for controller: {', '.join(arg)}"
        super().__init__(msg)


class WrongRouting(Exception):
    def __init__(self, path, current_handler_class, expected_handler_class):
        msg = f'Path {path} returned {current_handler_class.__name__} but {expected_handler_class.__name__} expected'
        super().__init__(msg)
