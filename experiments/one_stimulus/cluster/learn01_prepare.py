import numpy as np

import prepare


def compute_changes(params):
    changes = {'model': {'Hebbian': {}, 'RL': {}}}
    changes['model']['RL']['LTP'] = params['rl_ltp']
    changes['model']['RL']['LTD'] = 0.8*params['rl_ltp']
    changes['model']['Hebbian']['LTP'] = params['rl_ltp']/params['hebb_ratio']
    changes['model']['RL']['init'] = params['rl_init']

    return changes

def session(exp):
    """Day 1 with lesion, Day 2 without"""
    exp.model.setup()
    records = []

    # Day 1 : GPi OFF
    g1 = exp.model["GPi:cog -> THL:cog"].gain
    g2 = exp.model["GPi:mot -> THL:mot"].gain
    exp.model["GPi:cog -> THL:cog"].gain = 0
    exp.model["GPi:mot -> THL:mot"].gain = 0
    for trial in exp.task.block('choice'):
        exp.model.process(exp.task, trial)
    records.append(exp.task.records)

    # Day 2: GPi ON
    exp.model["GPi:cog -> THL:cog"].gain = g1
    exp.model["GPi:mot -> THL:mot"].gain = g2
    for trial in exp.task.block('choice'):
        exp.model.process(exp.task, trial)
    records.append(exp.task.records)

    return records


if __name__ == '__main__':
    prepare.copy_json('.')
    for idx, params in enumerate(prepare.param_generator()):
        changes = compute_changes(params)
        prepare.write_changes(idx, changes)
