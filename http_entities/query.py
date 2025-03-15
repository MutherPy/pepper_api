from dataclasses import dataclass
from bases.http_entities.query import BaseQuery
from urllib.parse import parse_qs


@dataclass
class Query(BaseQuery):
    def get(self, key: str):
        return self._query.get(key)

    def to_dict(self):
        return self._query

    @classmethod
    def from_scope(cls, scope: dict):
        if query_string := scope["query_string"]:
            parsed = parse_qs(query_string.decode("UTF-8"))
            for k in parsed:
                parsed[k] = parsed[k][0]
            return cls(parsed)
        return cls()
