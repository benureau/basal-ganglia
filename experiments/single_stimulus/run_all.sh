#!/bin/bash
# qsub needs Python 2 on the avakas cluster
export PYENV_VERSION=2.7.12
qsub -t 0-1616 launch_job.pbs
unset PYENV_VERSION
