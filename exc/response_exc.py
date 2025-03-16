
class UnprocessableEntity(Exception):
    def __init__(self, ent):
        msg = f"{type(ent)} can not be processed"
        super().__init__(msg)
