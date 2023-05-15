from datetime import datetime

import pytest

from repository import Link, InMemoryLinkRepository


@pytest.fixture
def repository():
    return InMemoryLinkRepository()


def test_repository_is_empty(repository):
    assert repository.get() == []


def test_create(repository):
    link = Link(url="test_url", hash_id="abc", created_at=datetime.utcnow())
    created_link = repository.create(link)
    assert link == created_link


def test_get_single_link(repository):
    link = Link(url="test_url", hash_id="abc", created_at=datetime.utcnow())
    created_link = repository.create(link)
    retrieved_link = repository.get(link.hash_id)

    assert created_link == retrieved_link


def test_get_not_exist_hash(repository):
    assert True


def test_create_duplicate_hash(repository):
    assert True
