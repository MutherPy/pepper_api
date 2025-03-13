
class IncorrectRegistering(Exception):
    def __init__(self, cls):
        msg = f'{cls.__name__} already registered.'
        super().__init__(msg)


class MissedRegistering(Exception):
    def __init__(self, cls_type):
        msg = f'"{cls_type}" missed in register table.'
        super().__init__(msg)
