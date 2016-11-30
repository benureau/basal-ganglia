import os, sys
import argparse

import config
from paths import rootdir
from prepare import param_generator


parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action='store_true')
args = parser.parse_known_args()[0]


# check missing files
missing = set()
for idx, params in enumerate(param_generator()):
    for filepath in [os.path.join(rootdir, 'data/data_{}.{:05d}.npy'.format(config.name, idx)),
                     os.path.join(rootdir, 'data/data_{}.{:05d}.txt'.format(config.name, idx)),
                     os.path.join(rootdir, 'data/changes_{}.{:05d}.json'.format(config.name, idx)),
                     #os.path.join(rootdir, 'data/data_{}.out-{}'.format(config.name, idx)),
                     #os.path.join(rootdir, 'data/data_{}.err-{}'.format(config.name, idx))
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
    cmd = './run_all.sh {} {}'.format(sys.argv[1], ','.join(cmd_idx))
    print("\nTo run incomplete jobs (assuming no job is still running), run:\n{}".format(cmd))


if args.verbose:
    for idx, n_trial, cue_freq, rew_freq in param_generator()[-1]:
        filepath = os.path.join(rootdir, 'data/data_{}.err-{}'.format(config.name, idx))
        if os.path.exists(filepath):
            stats = os.stat(filepath)
            if stats.st_size > 0:
                print('error: error file `{}` not empty'.format(filepath))
                with open(filepath) as fp:
                    print(fp.read())
