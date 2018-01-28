#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import shutil
import subprocess
import transcriber_re



wordSet = set([])

repo_name="test"
                
                
src_dir = "../"+repo_name+"_repo"
for corpus_dir in os.listdir(src_dir):
    if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
       print(corpus_dir)
       with open(src_dir + "/../target/_"+corpus_dir+"_"+repo_name+"_word.txt", "rb") as infile:
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
        print ("key= " + key)
        value = transcriber.transcribe(key)
        #print (key.encode("utf-8"))
        phonemeSet.update(value.split(" "))
        output = "{}\t{}\n".format(key.encode("utf-8"), value.encode("utf-8"))
        print (output.strip())
        outfile.write(output)


with open("../target/liepa.phone", "wb") as outfile:
    outfile.write("SIL\n")
    #outfile.write("SILPAUSE\n")
    #outfile.write("SILBREIN\n")
    #outfile.write("SILBREOUT\n")
    for phone in sorted(phonemeSet):
        outfile.write(phone + "\n")
