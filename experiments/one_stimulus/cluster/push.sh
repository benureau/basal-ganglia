#!/bin/bash

# push code to the cluster
rsync -azv --delete \
      --exclude *.so \
      --exclude *.c \
      --exclude *.txt \
      --exclude *.npy \
      --exclude *.pyc \
      --exclude *.egg-info \
      --exclude *.trace \
      --exclude .git/ \
      --exclude data/ \
      --exclude __pycache__/ \
      ../../.. avakas:monkeys/
