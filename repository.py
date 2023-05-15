from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Union, Iterable


@dataclass
class Link:
    url: str
    hash_id: str
    created_at: datetime


class LinkRepository:
    pass


class InMemoryLinkRepository(LinkRepository):
    def __init__(self):
        self._links: Dict[str, Link] = {}

    def get(self, hash_id: Optional[str] = None) -> Union[Iterable[Link], Link]:
        if hash_id is None:
            return list(self._links.values())
        else:
            return self._links[hash_id]

    def create(self, link: Link) -> Link:
        self._links[link.hash_id] = link
        return link


repository = InMemoryLinkRepository()
