# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import os

# adjusting path to find the library
import dotdot
from experiment import Experiment


def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(exp.task, trial)
    return exp.task.records

def time_guthrie():
    experiment = Experiment(model  = "../../experiments/model-guthrie.json",
                            task   = "../../experiments/task-guthrie.json",
                            result = "data/bench_guthrie.npy",
                            report = "data/bench_guthrie.txt",
                            n_session = 8, n_block = 1, seed = 1,
                            rootdir=os.path.dirname(__file__))
    records = experiment.run(session, save=False, force=True, parse=False)
    records = np.squeeze(records)


if __name__ == '__main__':
    time_guthrie()
