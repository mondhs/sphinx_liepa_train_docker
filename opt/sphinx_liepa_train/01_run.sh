#!/bin/bash
echo `date +"%T"`
SECONDS=0
sphinxtrain run
duration=$SECONDS
echo `date +"%T"`
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
