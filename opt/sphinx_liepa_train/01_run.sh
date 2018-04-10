#!/bin/bash
echo `date +"%T"`
SECONDS=0

if [ "$(ls -A ./feat)" ]; then
    # skip feature calcuation. 
    sphinxtrain -f verify run
else
    #Feature folder does not exists. act as normal
    sphinxtrain run
fi


duration=$SECONDS
echo `date +"%T"`
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
