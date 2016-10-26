import os
import argparse

from paths import rootdir
from prepare import param_generator


parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action='store_true')
args = parser.parse_args()


# check missing files
missing = set()
for idx, n_trial, cue_freq, rew_freq in param_generator()[-1]:
    for filepath in [os.path.join(rootdir, 'data/data_sgstim.{}.npy'.format(idx)),
                     os.path.join(rootdir, 'data/data_sgstim.{}.txt'.format(idx)),
                     os.path.join(rootdir, 'data/task_sgstim.{}'.format(idx)),
                     #os.path.join(rootdir, 'data/data_sgstim.out-{}'.format(idx)),
                     #os.path.join(rootdir, 'data/data_sgstim.err-{}'.format(idx))
                    ]:
        if not os.path.exists(filepath):
            print('error: `{}` not found'.format(filepath))
            missing.add(idx)

# generate qsub command for incomplete jobs
if len(missing) > 0:
    missing = sorted(missing)
    array_idx = []
    for i, idx in enumerate(missing):
        if i != 0 and missing[i-1] == idx - 1:
            array_idx[-1].append(idx)
        else:
            array_idx.append([idx])
    cmd_idx = []
    for idx in array_idx:
        if len(idx) == 1:
            cmd_idx.append('{}'.format(idx[0]))
        else:
            cmd_idx.append('{}-{}'.format(idx[0], idx[-1]))
    cmd = './run_all.sh {}'.format(','.join(cmd_idx))
    print("\nTo run incomplete jobs (assuming no job is still running), run:\n{}".format(cmd))


if args.verbose:
    for idx, n_trial, cue_freq, rew_freq in param_generator()[-1]:
        filepath = os.path.join(rootdir, 'data/data_sgstim.err-{}'.format(idx))
        if os.path.exists(filepath):
            stats = os.stat(filepath)
            if stats.st_size > 0:
                print('error: error file `{}` not empty'.format(filepath))
                with open(filepath) as fp:
                    print(fp.read())
