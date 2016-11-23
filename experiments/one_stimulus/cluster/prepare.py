import os
import json
import string
import shutil

import numpy as np

import config
from paths import rootdir


# json brackets are doubled, `{{`, to escape them from the format() function.
TASK_JSON = """
{{
    "session" : ["single", "choice"],
    "single" : {{
        "n_trial" : {n_trial},
        "n_cue"   : 1,
        "cue"     : [ {cue_freq_a}, {cue_freq_b},    0,    0 ],
        "pos"     : [    1,    1,    1,    1 ],
        "rwd"     : [ {rew_freq_a}, {rew_freq_b}, 0.00, 0.00 ]
    }},
    "choice" : {{
        "n_trial" : 100,
        "n_cue"   : 2,
        "cue"     : [    1,    1,    0,    0 ],
        "pos"     : [    1,    1,    1,    1 ],
        "rwd"     : [ {rew_freq_a}, {rew_freq_b}, 0.00, 0.00 ]
    }}
}}
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

    filename = 'task_{}.{}'.format(config.name, idx)
    path = os.path.join(rootdir, 'data')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'w') as f:
        f.write(content)

def copy_json(path):
    """Copy the base model and task json file"""
    # model
    model_path_from = os.path.join(path, config.params['model_base'])
    model_path_to   = os.path.join(rootdir, 'model_{}.json'.format(config.name))
    if not os.path.exists(os.path.dirname(model_path_to)):
        os.makedirs(os.path.dirname(model_path_to))
    shutil.copyfile(model_path_from, model_path_to)

    # task
    task_path_from = os.path.join(path, config.params['task_base'])
    task_path_to   = os.path.join(rootdir, 'task_{}.json'.format(config.name))
    if not os.path.exists(os.path.dirname(task_path_to)):
        os.makedirs(os.path.dirname(task_path_to))
    shutil.copyfile(task_path_from, task_path_to)

def param_generator():
    n_trials  = [0, 10, 20, 50, 100]
    cue_freqs = np.linspace(0.0, 1.0, 21)
    rew_freqs = np.linspace(0.0, 1.0, 21)

    params = []
    idx = 0
    for n_trial in n_trials:
        for cue_freq in cue_freqs:
            for rew_freq in rew_freqs:
                params.append((idx, n_trial, cue_freq, rew_freq))
                idx += 1
    return n_trials, cue_freqs, rew_freqs, params


if __name__ == "__main__":
    copy_json('.')
    for idx, n_trial, cue_freq, rew_freq in param_generator()[-1]:
        write_task_json(idx, n_trial, cue_freq, rew_freq)
