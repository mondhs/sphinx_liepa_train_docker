#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import sys
import subprocess
#reload(sys)
#sys.setdefaultencoding('utf-8')




wordSet = set([])

src_dir = "../liepa_audio"
with open("../target/liepa_train.fileids", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir + "/train"):
        if(os.path.isdir(os.path.join(src_dir, "train" ,corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_train.fileids", "rb") as infile:
                for line in infile:
                    outfile.write(line)

with open("../target/liepa_test.fileids", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir + "/test"):
        if(os.path.isdir(os.path.join(src_dir, "test" ,corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_test.fileids", "rb") as infile:
                for line in infile:
                    outfile.write(line)

#with open("../target/liepa_test.transcription", "wb") as outfile:
#    for corpus_dir in os.listdir(src_dir):
#        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
#           with open(src_dir + "/../target/_"+ corpus_dir+"_test.transcription", "rb") as infile:
#                for line in infile:
#                    outfile.write(line)

with open("../target/liepa_test_sil.transcription", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir+"/test"):
        if(os.path.isdir(os.path.join(src_dir, "test", corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_test.transcription", "rb") as infile:
                for line in infile:
                    line = line.decode("utf-8")
                    line = re.sub(r'\s{2,}',r" ",line)
                    #line = line.replace("\xef\xbb\xbf", "")
                    line = line.replace(u"\ufeff", "")
                    outfile.write(line.encode("utf-8"))
                    

with open("../target/liepa_train_sil.transcription", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir+"/train"):
        if(os.path.isdir(os.path.join(src_dir, "train", corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_train.transcription", "rb") as infile:
                for line in infile:
                    line = line.decode("utf-8")
                    line = re.sub(r'\s{2,}',r" ",line)
                    #line = line.replace("\xef\xbb\xbf", "")
                    line = line.replace(u"\ufeff", "")
                    outfile.write(line.encode("utf-8"))

#with open(src_dir + "/../target/liepa.phone", "rb") as infile:
#    infile_content = infile.read().decode("utf-8")
#    infile_content = infile_content.replace(u"\ufeff", "AAA")
#    print "File: {}".format(infile_content.encode("utf-8"))


#with open("../target/liepa_all.transcription", "wb") as outfile:
#    for corpus_dir in os.listdir(src_dir):
#        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
#           with open(src_dir + "/../target/_"+ corpus_dir+"_test.transcription", "rb") as infile:
#                for line in infile:
#                    outfile.write(line)
#    for corpus_dir in os.listdir(src_dir):
#        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
#           with open(src_dir + "/../target/_"+ corpus_dir+"_train.transcription", "rb") as infile:
#                for line in infile:
#                    outfile.write(line)
