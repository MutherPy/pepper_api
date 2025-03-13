from dataclasses import dataclass
from inspect import signature


@dataclass
class BaseHTTPEntity:
    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in signature(cls).parameters
        })
