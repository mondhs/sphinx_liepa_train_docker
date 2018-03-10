#!/bin/bash


tar -czvf sphinx_log-$(date +%Y%m%dT%H%M%S).tar.gz liepa.html logdir result/ model_parameters/ && mv sphinx_log-* ./etc/arch
