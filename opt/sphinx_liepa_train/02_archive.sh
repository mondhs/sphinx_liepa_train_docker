#!/bin/bash


tar -czvf sphinx_log-$(date +%Y%m%dT%H%M%S).tar.gz liepa.html logdir result/ | mv sphinx_log-* ./etc/arch
rm liepa.html logdir result bwaccumdir model_* qmanager trees -rf
