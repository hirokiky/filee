from ftree.testing import OverrideSettings

import pytest


@pytest.fixture
def override_settings():
    with OverrideSettings() as os:
        yield os
