import re
from typing import Optional, Type

from src.core.bases.handler import BaseHandler
from src.core.bases.routing_struct import BaseRoutingStructure


class RadixNode:
    def __repr__(self):
        return f"{self.segment=} {self.children=} {self.param_child=}"

    def __init__(self, segment=""):
        self.segment = segment
        self.children = {}
        self.param_child = None
        self.param_name = None
        self.handler = None

    def insert(self, path_parts, handler):
        node = self
        for part in path_parts:
            match = re.fullmatch(r"\{([\w\d]+)}", part)
            if match:
                param_name = match.group(1)
                if not node.param_child:
                    node.param_child = RadixNode(":")
                    node.param_child.param_name = param_name
                node = node.param_child
            else:
                first_char = part[0]
                if first_char not in node.children:
                    node.children[first_char] = RadixNode(part)
                else:
                    existing_child = node.children[first_char]
                    common_prefix = self._common_prefix(existing_child.segment, part)
                    if common_prefix != existing_child.segment:
                        suffix_existing = existing_child.segment[len(common_prefix):]
                        suffix_new = part[len(common_prefix):]

                        new_parent = RadixNode(common_prefix)
                        new_parent.children[suffix_existing[0]] = existing_child
                        existing_child.segment = suffix_existing
                        node.children[first_char] = new_parent

                        if suffix_new:
                            new_parent.children[suffix_new[0]] = RadixNode(suffix_new)

                        node = new_parent
                        continue

                node = node.children[first_char]

        node.handler = handler

    def find(self, path_parts) -> tuple[Optional[Type[BaseHandler]], Optional[dict]]:
        node = self
        params = {}

        for part in path_parts:
            first_char = part[0]

            if first_char in node.children:
                child = node.children[first_char]
                if part == child.segment:
                    node = child
                    continue

            if node.param_child:
                params[node.param_child.param_name] = part
                node = node.param_child
                continue

            return None, {}

        return (node.handler, params) if node.handler else (None, None)

    @staticmethod
    def _common_prefix(s1, s2):
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]:
                return s1[:i]
        return s1[:min_len]


class RadixTree(BaseRoutingStructure):
    def __init__(self):
        self.root = RadixNode()

    def add_route(self, path: str, handler):
        path_parts = path.strip("/").split("/")
        self.root.insert(path_parts, handler)

    def find_handler(self, path: str) -> tuple[Optional[Type[BaseHandler]], Optional[dict]]:
        path_parts = path.strip("/").split("/")
        return self.root.find(path_parts)

    def show_routes(self):
        print(self.root.children)

