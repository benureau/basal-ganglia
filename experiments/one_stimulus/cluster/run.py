#import provenance
#provenance.init(strict=False) # TinyDB not compatible with multiple access!!!

import importlib
import sys
import numpy as np

import config
from paths import rootdir
from bg import Experiment



def run(config_path, task_id):
    """:param task_id: int"""
    session = importlib.import_module(config.params['python_module']).session

    experiment = Experiment(model  = 'model_{}.json'.format(config.name),
                            task   = 'task_{}.json'.format(config.name),
                            result = 'data/data_{}.{:05d}.pickle'.format(config.name, task_id),
                            report = 'data/data_{}.{:05d}.json'.format(config.name, task_id),
                            changes= 'data/changes_{}.{:05d}.json'.format(config.name, task_id),
                            n_session=config.params["n_sessions"],
                            rootdir=rootdir, seed=0, verbose=True)
    experiment.run(session, config.label, save=True, force=True)


if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]))
