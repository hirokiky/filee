from contextlib import contextmanager

from . import settings


@contextmanager
def override_settings(**new_settings):
    old_values = {}

    for k, v in new_settings.items():
        old = getattr(settings, k)
        old_values[k] = old
        setattr(settings, k, v)

    yield

    for k, v in old_values.items():
        setattr(settings, k, v)
