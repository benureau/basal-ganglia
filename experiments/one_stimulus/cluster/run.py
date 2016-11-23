import provenance
provenance.init(strict=False)

import sys
import numpy as np

import config
from paths import rootdir
from bg import Experiment


def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(task=exp.task, trial=trial, model=exp.model)
    return exp.task.records

def run(task_id):
    """:param task_id: int"""
    experiment = Experiment(model  = 'model_{}.json'.format(config.name),
                            task   = 'task_{}.json'.format(config.name),
                            result = 'data/data_{}.{:05d}.npy'.format(config.name, task_id),
                            report = 'data/data_{}.{:05d}.txt'.format(config.name, task_id),
                            n_session=config.params["n_sessions"], n_block=1, seed=0,
                            changes= 'changes_{}.{:05d}.json'.format(config.name, task_id),
                            verbose=True, rootdir=rootdir)
    experiment.run(session, config.label, save=True, force=False)


if __name__ == '__main__':
    run(int(sys.argv[2]))
