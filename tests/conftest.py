from filee.hasher import FileHasher
from filee.testing import OverrideSettings

import pytest


@pytest.fixture
def override_settings():
    with OverrideSettings() as os:
        yield os


@pytest.fixture
def hasher(tmpdir, override_settings):
    h = tmpdir.join('.fileeloadhashes')
    yield FileHasher(h.strpath)
