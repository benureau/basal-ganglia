import sys
import numpy as np

from paths import rootdir

import dotdot
from experiment import Experiment


def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(task=exp.task, trial=trial, model=exp.model)
    return exp.task.records

def run(task_id):
    experiment = Experiment(model  = "model-single-stimulus_nonhebb.json",
                            task   = "data/task_sgstim.{}".format(task_id),
                            result = "data/data_sgstim.{}.npy".format(task_id),
                            report = "data/data_sgstim.{}.txt".format(task_id),
                            n_session=100, n_block=1, seed=0,
                            verbose=True, rootdir=rootdir)
    experiment.run(session, "Single Stimulus",
                   save=True, force=False, parse=False)


if __name__ == '__main__':
    import os
    print(os.uname(), file=sys.stdout)
    run(sys.argv[1])
