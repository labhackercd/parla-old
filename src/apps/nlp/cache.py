from django.conf import settings
import shelve
import os


def load_from_cache(var_name, initial_value_method=None,
                    force_update=False, **kwargs):
    """Loads a variable from cache.db. If this variable does not exist
    `initial_value_method` is called and the return is used to set a intial
    to the variable on cache.
    If the variable name isn't in cache and anyone  initial value method is
    provided, return None.
    """
    db = shelve.open(os.path.join(settings.BASE_DIR, 'cache.db'))
    try:
        if force_update:
            raise KeyError
        else:
            return_value = db[var_name]
            db.close()
            return return_value
    except KeyError:
        if callable(initial_value_method):
            db[var_name] = initial_value_method(**kwargs)
            db.sync()
            return_value = db[var_name]
            db.close()
            return return_value
        else:
            return None


def update(var_name, value):
    """Update a variable with a new value or add a new variable to cache."""
    db = shelve.open(os.path.join(settings.BASE_DIR, 'cache.db'))
    db[var_name] = value
    db.sync()
    db.close()
