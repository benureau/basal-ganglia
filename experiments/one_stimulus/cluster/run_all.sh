#!/bin/bash
# qsub needs Python 2 on the avakas cluster
export PYENV_VERSION=2.7.12
INDICES="0-440"

if (( "$#" > 1 ))
then
  INDICES=$2;
fi

CMD="qsub -t ${INDICES} -F \"$1\" launch_job.pbs"
echo $CMD
eval $CMD
unset PYENV_VERSION
