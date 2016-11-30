import os
import json
import string
import shutil
import itertools

import numpy as np

import config
from paths import rootdir


# json brackets are doubled, `{{`, to escape them from the format() function.
# TASK_JSON = """
# {{
#     "session" : ["single", "choice"],
#     "single" : {{
#         "n_trial" : {n_trial},
#         "n_cue"   : 1,
#         "cue"     : [ {cue_freq_a}, {cue_freq_b},    0,    0 ],
#         "pos"     : [    1,    1,    1,    1 ],
#         "rwd"     : [ {rew_freq_a}, {rew_freq_b}, 0.00, 0.00 ]
#     }},
#     "choice" : {{
#         "n_trial" : 100,
#         "n_cue"   : 2,
#         "cue"     : [    1,    1,    0,    0 ],
#         "pos"     : [    1,    1,    1,    1 ],
#         "rwd"     : [ {rew_freq_a}, {rew_freq_b}, 0.00, 0.00 ]
#     }}
# }}
# """


def session(exp):
    """Default session function

    Run the task, by iterating over all trials.
    """
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(task=exp.task, trial=trial, model=exp.model)
    return exp.task.records


def write_changes(idx, changes):
    """Write the json file with the given parameters."""
    filename = 'changes_{}.{:05d}.json'.format(config.name, idx)
    path = os.path.join(rootdir, 'data')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'w') as fp:
        json.dump(changes, fp, indent=4, ensure_ascii=False)

def copy_json(path='.'):
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

def param_generator(param_ranges=None):
    """Generate all the parameter ranges.

    :param params_ranges: a dict of values that the parameters can take,
                          e.g. {'rl': [0.01, 0.02, 0.03], 'hebbian': [True, False]}
    """
    if param_ranges is None:
        param_ranges = config.params['params']

    sorted_keys = sorted(param_ranges.keys())
    combinations = itertools.product(*[param_ranges[k] for k in sorted_keys])
    param_comb = []
    for values in combinations:
        param_comb.append({k: v for k, v in zip(sorted_keys, values)})
    return param_comb
