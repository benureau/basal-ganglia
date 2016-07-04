import time
import multiprocessing

import numpy as np

import bench_dana
import bench_guthrie


funs = [('bench_dana.time_dana',       bench_dana.time_dana,       5),
        ('bench_guthrie.time_guthrie', bench_guthrie.time_guthrie, 3),
       ]
max_name = max(len(name) for name, fun, repeat in funs)


for name, fun, repeat in funs:
    durations = []

    for _ in range(repeat):
        start = time.time()
        p = multiprocessing.Process(target=fun)
        p.start()
        p.join()
        durations.append(time.time() - start)

    mean_dur = np.mean(durations)
    std_dur = np.std(durations)

    print('{}:{} {:.4f}s ± {:.4f}s'.format(name, ' '*(max_name-len(name)), mean_dur, std_dur))
