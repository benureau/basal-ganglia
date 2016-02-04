# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from experiment import Experiment

def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(exp.task, trial)
    return exp.task.records

def test_model():
    experiment = Experiment(model  = "experiments/model-guthrie.json",
                            task   = "experiments/task-guthrie.json",
                            result = "test-experiment-guthrie.npy",
                            report = "test-experiment-guthrie.txt",
                            n_session = 25, n_block = 1, seed = 1)
    records = experiment.run(session, save=False, force=True, parse=False)
    records = np.squeeze(records)    

    mean = np.mean(records["best"], axis=0)[-1]
    std  = np.std(records["best"], axis=0)[-1]
    print("Mean performance: %.2f ± %.2f" % (mean, std))
    print("-"*30)

    
    assert mean >= 0.85
