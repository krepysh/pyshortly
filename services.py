from urllib import parse
from datetime import datetime

from repository import Link, repository
from werkzeug.security import generate_password_hash


class InvalidUrl(Exception):
    pass


def validate_url(url):
    schema, netloc, *_ = parse.urlparse(url)
    if not schema or not netloc:
        raise InvalidUrl


def create_short_url(url: str) -> Link:
    validate_url(url)
    new_hash = generate_password_hash(url, method="pbkdf2:sha256:6")[-6:]
    new_link = Link(url=url, hash_id=new_hash, created_at=datetime.utcnow())
    new_link = repository.create(new_link)
    return new_link
