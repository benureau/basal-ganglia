import os
import json
import string

import numpy as np

from paths import rootdir


TASK_JSON = """
(
    "session" : ["single", "choice"],
    "single" : (
        "n_trial" : {n_trial},
        "n_cue"   : 1,
        "cue"     : [ {cue_freq_a}, {cue_freq_b},    0,    0 ],
        "pos"     : [    1,    1,    1,    1 ],
        "rwd"     : [ {rew_freq_a}, {cue_freq_b}, 0.00, 0.00 ]
    ),
    "choice" : (
        "n_trial" : 100,
        "n_cue"   : 2,
        "cue"     : [    1,    1,    0,    0 ],
        "pos"     : [    1,    1,    1,    1 ],
        "rwd"     : [ {rew_freq_a}, {cue_freq_b}, 0.00, 0.00 ]
    )
)
"""


def write_task_json(idx, n_trial, cue_freq_a, rew_freq_a,
                    cue_freq_b=None, rew_freq_b=None):
    """Write the json file with the given parameters."""
    if cue_freq_b is None:
        cue_freq_b = 1.0 - cue_freq_a
    if rew_freq_b is None:
        rew_freq_b = 1.0 - rew_freq_a
    content = TASK_JSON.format(n_trial=n_trial, cue_freq_a=cue_freq_a,
        rew_freq_a=rew_freq_a, cue_freq_b=cue_freq_b, rew_freq_b=rew_freq_b)
    content = content.replace('(', '{')
    content = content.replace(')', '}')

    filename = 'task_sgstim.{}'.format(idx)
    path = os.path.join(rootdir, 'data')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'w') as f:
        f.write(content)

def copy_model_json(src):
    with open(src, 'r') as f:
        content = f.read()

    filepath = os.path.join(rootdir, 'model.json')
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    idx = 0
    for n_trial in [5, 10, 20, 30, 50, 100, 200]:
        for cue_freq in np.linspace(0.5, 1.0, 11):
            for rew_freq in np.linspace(0.0, 1.0, 21):
                write_task_json(idx, n_trial, cue_freq, rew_freq)
                idx += 1
    copy_model_json('model.json')
