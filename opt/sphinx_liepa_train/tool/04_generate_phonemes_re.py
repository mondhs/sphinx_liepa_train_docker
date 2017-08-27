#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import shutil
import subprocess
import transcriber_re



wordSet = set([])

src_dir = "../liepa_audio"
for corpus_dir in os.listdir(src_dir+"/test"):
    if(os.path.isdir(os.path.join(src_dir, "test" ,corpus_dir))):
       print corpus_dir
       with open(src_dir + "/../target/_"+ corpus_dir+"_word.txt", "rb") as infile:
            for line in infile:
                line = line.decode("utf-8")
                line = line.replace(u"\ufeff", "")
                line = line.rstrip()
                line=re.sub(r'<sil[\+\w]*>',r'',line)
                wordSet.add(line)
                
                
for corpus_dir in os.listdir(src_dir+"/train"):
    if(os.path.isdir(os.path.join(src_dir, "train" ,corpus_dir))):
       print corpus_dir
       with open(src_dir + "/../target/_"+ corpus_dir+"_word.txt", "rb") as infile:
            for line in infile:
                line = line.decode("utf-8")
                line = line.replace(u"\ufeff", "")
                line = line.rstrip()
                line=re.sub(r'<sil[\+\w]*>',r'',line)
                wordSet.add(line)

wordSet.remove("")

wordList = sorted(list(wordSet))

wordsStr = "\n".join(wordList)
#print ">>>> wordsStr\n" + wordsStr

#automagical transformation
transcriber = transcriber_re.TranscriberRegexp()

phonemeSet = set([])

with open("../target/liepa_zodziai.csv", "wb") as outfile:
    for word in wordList:
        outfile.write(word.encode("utf-8") + "\n")

with open("../target/liepa.dic", "wb") as outfile:
    for i in range(len(wordList)):
        key = wordList[i]
        #print key
        value = transcriber.transcribe(key.encode("utf-8"))
        print key.encode("utf-8")
        phonemeSet.update(value.split(" "))
        output = "{}\t{}\n".format(key.encode("utf-8"), value.encode("utf-8"))
        print output.strip()
        outfile.write(output)


with open("../target/liepa.phone", "wb") as outfile:
    outfile.write("SIL\n")
    #outfile.write("SILPAUSE\n")
    #outfile.write("SILBREIN\n")
    #outfile.write("SILBREOUT\n")
    for phone in sorted(phonemeSet):
        outfile.write(phone + "\n")
