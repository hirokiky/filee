from ftree.hasher import FileHasher

import pytest


@pytest.fixture
def main_path(tmpdir):
    return tmpdir.join('main.py').strpath


def test_hash_changed(tmpdir, main_path):
    fh = FileHasher(
        tmpdir.join('hashes').strpath,
        {main_path: '7984fc60703f0e3801005e042bb13c86'})

    actual = fh.has_changed(main_path, b'This content has been changed\n')
    assert actual
    assert fh.changed
    assert fh.hashes == {main_path: 'cdff386470e43287d36ca6eb377e93fa'}


def test_hash_changed_not_existed(tmpdir, main_path):
    fh = FileHasher(
        tmpdir.join('hashes').strpath,
        {})

    actual = fh.has_changed(main_path, b'import this\n')
    assert actual
    assert fh.changed
    assert fh.hashes == {main_path: '7984fc60703f0e3801005e042bb13c86'}


def test_hash_changed_not_changed(tmpdir, main_path):
    fh = FileHasher(
        tmpdir.join('hashes').strpath,
        {main_path: '7984fc60703f0e3801005e042bb13c86'})

    actual = fh.has_changed(main_path, b'import this\n')
    assert not actual
    assert not fh.changed
    assert fh.hashes == {main_path: '7984fc60703f0e3801005e042bb13c86'}
