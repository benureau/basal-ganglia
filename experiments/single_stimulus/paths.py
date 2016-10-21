"""You should edit this file to your path configuration"""
import os


if (os.uname()[0] == 'Linux' and
    (   os.uname()[1].startswith('avakas')
     or os.uname()[1].startswith('node')
     or os.uname()[1].startswith('bigmem'))): # for the avakas cluster
    rootdir = '/scratch/fbenurea/monkeys/sgstim_dual'
elif os.uname()[0] == 'Darwin' and os.uname()[1] == 'im-e7-fabien': # fabien's machine
    rootdir = '~/research/data/monkeys/sgstim_dual'
else:
    raise Exception("No matching system for defining paths with uname: {}".format(os.uname()))

rootdir = os.path.expanduser(rootdir)
