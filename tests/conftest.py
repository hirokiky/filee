from ftree.hasher import FileHasher
from ftree.testing import OverrideSettings

import pytest


@pytest.fixture
def override_settings():
    with OverrideSettings() as os:
        yield os


@pytest.fixture
def hasher(tmpdir, override_settings):
    h = tmpdir.join('.ftreeloadhashes')
    yield FileHasher(h.strpath)
