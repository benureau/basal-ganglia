import numpy as np

import prepare
import learn01_prepare


compute_changes = learn01_prepare.compute_changes

def session(exp):
    """Day 1 without lesion, Day 2 with one"""
    exp.model.setup()
    records = []

    # Day 1 : GPi ON
    for trial in exp.task.block('choice'):
        exp.model.process(exp.task, trial)
    records.append(exp.task.records)

    # Day 2: GPi OFF
    exp.model["GPi:cog -> THL:cog"].gain = 0
    exp.model["GPi:mot -> THL:mot"].gain = 0
    for trial in exp.task.block('choice'):
        exp.model.process(exp.task, trial)
    records.append(exp.task.records)

    return records


if __name__ == '__main__':
    prepare.copy_json('.')
    for idx, params in enumerate(prepare.param_generator()):
        changes = compute_changes(params)
        prepare.write_changes(idx, changes)
