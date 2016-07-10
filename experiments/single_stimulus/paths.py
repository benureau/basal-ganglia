"""You should edit this file to your path configuration"""
import os


if (os.uname()[0] == 'Linux' and
    (os.uname()[1].startswith('node') or os.uname()[1].startswith('avakas'))): # for the avakas cluster
    rootdir = '/scratch/fbenurea/monkeys/sgstim/'
elif os.uname()[0] == 'Darwin' and os.uname()[1] == 'im-e7-fabien': # fabien's machine
    rootdir = '~/research/data/monkeys/sgstim'
else:
    raise Exception("No matching system for defining paths")

rootdir = os.path.expanduser(rootdir)
