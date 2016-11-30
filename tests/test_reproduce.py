# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import os
import unittest
import numpy as np

import dotdot
import bg


filename = 'data/guthrie_result'

def run_model():
    experiment = bg.Experiment(model  = "../experiments/guthrie/guthrie_model.json",
                               task   = "../experiments/guthrie/guthrie_task.json",
                               result = "{}.npy".format(filename),
                               report = "{}.txt".format(filename),
                               n_session = 8, n_block = 1, seed = 1,
                               rootdir=os.path.dirname(__file__),
                               verbose=False) # for unittest and nosetests.
    records = experiment.run(bg.session, save=True, force=True)

def result_filename(suffix='', ext='npy'):
    return os.path.join(os.path.dirname(__file__),
                        '{}{}.{}'.format(filename, suffix, ext))


class DanaTests(unittest.TestCase):
    """Verifying that results can be reproduced exactly."""

    def test_reproducible(self):
        # removing existing results
        for ext in ['npy', 'txt']:
            for suffix in ['', '_ref']:
                if os.path.exists(result_filename(suffix=suffix, ext=ext)):
                    os.remove(result_filename(suffix=suffix, ext=ext))

        # first run of the model
        run_model()
        # moving the files out of the way
        for ext in ['npy', 'txt']:
            os.rename(result_filename(ext=ext), result_filename(suffix='_ref', ext=ext))
        # second run of the model: should be identical
        run_model()

        # comparing results
        for ext in ['npy', 'txt']:
            with open(result_filename(ext=ext), 'rb') as f:
                run0 = f.read()
            with open(result_filename(suffix='_ref', ext=ext), 'rb') as f:
                run1 = f.read()
            assert run0 == run1


if __name__ == '__main__':
    unittest.main()
