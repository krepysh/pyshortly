from datetime import datetime

import pytest

from repository import Link, InMemoryLinkRepository, FileSystemLinkRepository


@pytest.fixture
def repository_in_mem():
    return InMemoryLinkRepository()


@pytest.fixture
def fs_repository(tmp_path):
    return FileSystemLinkRepository(tmp_path)


def test_repository_is_empty(repository_in_mem):
    assert repository_in_mem.get() == []


def test_create(repository_in_mem):
    link = Link(url="test_url", hash_id="abc", created_at=datetime.utcnow())
    created_link = repository_in_mem.create(link)
    assert link == created_link


def test_get_single_link(repository_in_mem):
    link = Link(url="test_url", hash_id="abc", created_at=datetime.utcnow())
    created_link = repository_in_mem.create(link)
    retrieved_link = repository_in_mem.get(link.hash_id)

    assert created_link == retrieved_link


def test_get_not_exist_hash(repository_in_mem):
    assert True


def test_create_duplicate_hash(repository_in_mem):
    assert True


def test_create_in_fs(fs_repository):
    fs_repository.create(
        Link(url="test_link", hash_id="hash", created_at=datetime(2023, 5, 15))
    )
    link = fs_repository.get("hash")
    links = fs_repository.get()

    assert link.url == "test_link"
    assert len(links) == 1
    assert links[0].url == "test_link"


def test_link_with_datetime_fs(fs_repository):
    link = Link(url="test_url", hash_id="abc", created_at=datetime.utcnow())
    fs_repository.create(link)

    gotten_link = fs_repository.get("abc")
    assert isinstance(gotten_link.created_at, datetime)
