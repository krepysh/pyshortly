from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Union, Iterable, overload


@dataclass
class Link:
    url: str
    hash_id: str
    created_at: datetime


class LinkRepository(ABC):
    @overload
    def get(self) -> Iterable[Link]:
        ...

    @overload
    def get(self, hash_id: str) -> Link:
        ...

    @abstractmethod
    def get(self, hash_id: Optional[str] = None) -> Union[Iterable[Link], Link]:
        pass

    @abstractmethod
    def create(self, link: Link) -> Link:
        pass


class InMemoryLinkRepository(LinkRepository):
    def __init__(self) -> None:
        self._links: Dict[str, Link] = {}

    @overload
    def get(self) -> Iterable[Link]:
        ...

    @overload
    def get(self, hash_id: str) -> Link:
        ...

    def get(self, hash_id: Optional[str] = None) -> Union[Iterable[Link], Link]:
        if hash_id is None:
            return list(self._links.values())
        else:
            return self._links[hash_id]

    def create(self, link: Link) -> Link:
        self._links[link.hash_id] = link
        return link


repository = InMemoryLinkRepository()
