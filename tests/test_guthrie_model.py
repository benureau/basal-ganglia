# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import os

import dotdot
import bg


def test_model():
    experiment = bg.Experiment(model  = "../experiments/guthrie/guthrie_model.json",
                               task   = "../experiments/guthrie/guthrie_task.json",
                               result = "data/guthrie_result.pickle",
                               report = "data/guthrie_report.json",
                               n_session = 25, seed = 1,
                               rootdir=os.path.dirname(__file__),
                               verbose=False)
    records = experiment.run(bg.session, save=False, force=True)
    records = np.squeeze(records)

    mean = np.mean(records["best"], axis=0)[-1]
    std  = np.std(records["best"], axis=0)[-1]
    print("Mean performance: %.2f ± %.2f" % (mean, std))
    print("-"*30)

    assert mean >= 0.75

if __name__ == "__main__":
    test_model()
