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
    experiment = Experiment(model  = 'model_{}.json'.format(config.name),
                            task   = 'data/task_{}.{}'.format(config.name, task_id),
                            result = 'data/data_{}.{}.npy'.format(config.name, task_id),
                            report = 'data/data_{}.{}.txt'.format(config.name, task_id),
                            n_session=100, n_block=1, seed=0,
                            verbose=True, rootdir=rootdir)
    experiment.run(session, config.label, save=True, force=False)


if __name__ == '__main__':
    run(sys.argv[2])
