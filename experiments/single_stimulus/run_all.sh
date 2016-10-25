#!/bin/bash
# qsub needs Python 2 on the avakas cluster
export PYENV_VERSION=2.7.12
INDICES="0-1847"

if (( "$#" > 0 ))
then
  INDICES=$1;
fi

CMD="qsub -t ${INDICES} launch_job.pbs"
echo $CMD
eval $CMD
unset PYENV_VERSION
