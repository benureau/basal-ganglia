import os
import json
import collections


def filepath(rootdir, filename):
    """Return the absolute filepath"""
    return os.path.abspath(os.path.join(rootdir, filename))

def load_json(rootdir, filename):
    """Load the json file and return a dict."""
    path = filepath(rootdir, filename)
    with open(path, 'r') as fp:
        params = json.load(fp)
    return params

def update_json(original, update):
    """Update a json dictionary of varying depth with the content of another.

    The element to update must exist in the original dictionary.

    if
    > original = {'a': {'key_a': 1, 'key_b': 2}, 'b': 3}
    > update   = {'a': {'key_b': 5}}
    then
    > update_json(original, update)
    is equal to {'a': {'key_a': 1, 'key_b': 5}, 'b': 3}
    """
    for k, v in update.items():
        assert k in original
        if isinstance(v, collections.Mapping):
            original[k] = update_json(original[k], v)
        else:
            original[k] = update[k]
    return original


if __name__ == '__main__':
    original = {'a': {'key_a': 1, 'key_b': 2}, 'b': 3}
    update   = {'a': {'key_b': 5}}
    assert update_json(original, update) == {'a': {'key_a': 1, 'key_b': 5}, 'b': 3}
