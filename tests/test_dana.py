import unittest
import numpy as np

import dotdot
from bg import dana

class DanaTests(unittest.TestCase):
    """Verifying that cdana behaves as expected."""

    def test_group_random(self):
        """Verifying that delta correct"""
        group = dana.Group(4)
        group['V'] = np.array([0.0, 1.0, 2.0, 3.0])
        group.evaluate(0.001)
        self.assertTrue(np.allclose(group.delta, 0.9))

        group = dana.Group(4, activation=dana.Clamp(-1.0, 1.0))
        group['V'] = np.array([0.0, -1.0, -2.0, -3.0])
        group.evaluate(0.001)
        self.assertTrue(np.allclose(group.delta, 0.9))


if __name__ == '__main__':
    unittest.main()
