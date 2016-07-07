import sys
import time
import numpy as np

import dotdot

if len(sys.argv) > 1:
    if sys.argv[1] == 'pydana':
        from cdana import pydana
        mod = dana
    else:
        import cdana
        mod = cdana
else:
    import cdana
    mod = cdana


def bench_connections(K=2000, L=1000):
    """Test all 1D connections"""

    for con, src_shape, tgt_shape, weights_shape in [
        (mod.OneToOne,  4,  4,  4),
        (mod.OneToAll,  4,  4,  4),
        (mod.AssToMot, 16,  4,  4),
        (mod.AssToCog, 16,  4,  4),
        (mod.MotToAss,  4, 16,  4),
        (mod.CogToAss,  4, 16,  4),
        (mod.AllToAll,  4,  4, 16),

        #(mod.AssToMot, cdana.AssToMot, 16, 4, 4),
        ]:


        for _ in range(K):
            source  = np.random.rand(src_shape)
            target  = np.random.rand(tgt_shape)
            weights = np.random.rand(weights_shape)
            gain    = np.random.random()

            c = con(np.copy(source), np.copy(target), np.copy(weights), gain)
            for _ in range(L):
                c.propagate()

def bench_group(K=1000, L=100):

    for _ in range(K):
        dt = np.random.uniform(low=-0.1, high=0.1)
        group  = cdana.Group(4)
        group['V']    = np.random.random(group['V'].shape)
        group['Iext'] = np.random.random(group['Iext'].shape)
        group['Isyn'] = np.random.random(group['Isyn'].shape)

        for i in range(L):
            group.evaluate(dt)


def time_dana():
    np.random.seed(0)
    bench_connections(K=4000, L=1000)
    bench_group(K=2000, L=100)
