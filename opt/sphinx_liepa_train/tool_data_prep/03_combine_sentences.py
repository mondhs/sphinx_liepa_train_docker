#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import sys
import subprocess
#reload(sys)
#sys.setdefaultencoding('utf-8')



train_repo_name="train"
test_repo_name="test"

wordSet = set([])

def processRepo(repo_name):
    src_dir = "../"+repo_name+"_repo/"


    with open("../target/liepa_"+repo_name+".fileids", "w") as outfile:
        for corpus_dir in os.listdir(src_dir):
            if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
               with open(src_dir + "/../target/_"+ corpus_dir+"_"+repo_name+".fileids", "r") as infile:
                    for line in infile:
                        outfile.write(line)



    with open("../target/liepa_"+repo_name+"_sil.transcription", "w") as outfile:
        for corpus_dir in os.listdir(src_dir):
            if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
               with open(src_dir + "/../target/_"+ corpus_dir+"_"+repo_name+".transcription", "r") as infile:
                    for line in infile:
                        # line = line.decode("utf-8")
                        line = re.sub(r'\s{2,}',r" ",line)
                        # line = line.replace(u"\ufeff", "")
                        outfile.write(line)


if __name__ == "__main__":
    processRepo(test_repo_name)
    processRepo(train_repo_name)
