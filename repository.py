import dataclasses
import json
import os
from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Union, overload, List


@dataclass
class Link:
    url: str
    hash_id: str
    created_at: datetime


class LinkRepository(ABC):
    @overload
    def get(self) -> List[Link]:
        ...

    @overload
    def get(self, hash_id: str) -> Link:
        ...

    @abstractmethod
    def get(self, hash_id: Optional[str] = None) -> Union[List[Link], Link]:
        pass

    @abstractmethod
    def create(self, link: Link) -> Link:
        pass


class InMemoryLinkRepository(LinkRepository):
    def __init__(self) -> None:
        self._links: Dict[str, Link] = {}

    @overload
    def get(self) -> List[Link]:
        ...

    @overload
    def get(self, hash_id: str) -> Link:
        ...

    def get(self, hash_id: Optional[str] = None) -> Union[List[Link], Link]:
        if hash_id is None:
            return list(self._links.values())
        else:
            return self._links[hash_id]

    def create(self, link: Link) -> Link:
        self._links[link.hash_id] = link
        return link


class FileSystemLinkRepository(LinkRepository):
    def __init__(self, path: Union[str, Path]):
        self.path = os.path.join(path, "db")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def create(self, link: Link) -> Link:
        with open(os.path.join(self.path, f"{link.hash_id}.txt"), "x") as f:
            json.dump(dataclasses.asdict(link), fp=f)
        return link

    @overload
    def get(self) -> List[Link]:
        ...

    @overload
    def get(self, hash_id: str) -> Link:
        ...

    def get(self, hash_id: Optional[str] = None) -> Union[Link, List[Link]]:
        if hash_id is not None:
            return self._read_single_link(hash_id)
        else:
            links = []
            for filename in os.listdir(self.path):
                hash_id = filename.removesuffix(".txt")
                link = self._read_single_link(hash_id)
                links.append(link)
            return links

    def _read_single_link(self, hash_id):
        with open(os.path.join(self.path, f"{hash_id}.txt")) as f:
            link_json = json.load(f)
            link = Link(
                url=link_json["url"],
                hash_id=link_json["hash_id"],
                created_at=link_json["created_at"],
            )
        return link


repository = InMemoryLinkRepository()
