import os

from paths import rootdir
from prepare import param_generator


for idx, n_trial, cue_freq, rew_freq in param_generator():
    for filepath in [os.path.join(rootdir, 'data/data_sgstim.{}.npy'.format(idx)),
                     os.path.join(rootdir, 'data/data_sgstim.{}.txt'.format(idx)),
                     os.path.join(rootdir, 'data/task_sgstim.{}'.format(idx)),
                     os.path.join(rootdir, 'data/data_sgstim.out-{}'.format(idx)),
                     os.path.join(rootdir, 'data/data_sgstim.err-{}'.format(idx))]:
        if not os.path.exists(filepath):
            print('error: `{}` not found'.format(filepath))


for idx, n_trial, cue_freq, rew_freq in param_generator():
    filepath = os.path.join(rootdir, 'data/data_sgstim.err-{}'.format(idx))
    if os.path.exists(filepath):
        stats = os.stat(filepath)
        if stats.st_size > 0:
            print('error: error file `{}` not empty'.format(filepath))
            with open(filepath) as fp:
                print(fp.read())
