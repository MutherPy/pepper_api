
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
