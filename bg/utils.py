import os
import json


def filepath(rootdir, filename):
    """Return the absolute filepath"""
    return os.path.abspath(os.path.join(rootdir, filename))

def load_json(rootdir, filename):
    """Load the json file and return a dict."""
    path = filepath(rootdir, filename)
    with open(filename, 'r') as fp:
        params = json.load(fp)
    return params
