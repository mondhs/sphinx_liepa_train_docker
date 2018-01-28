#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import shutil
import subprocess
import transcriber_re
from io import open


#automagical transformation
transcriber = transcriber_re.TranscriberRegexp()

wordSet = set([])

train_repo_name="train"
test_repo_name="test"

def readRepo(repo_name):
    src_dir = "../"+repo_name+"_repo"
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           print(corpus_dir)
           with open(src_dir + "/../target/_"+corpus_dir+"_"+repo_name+"_word.txt", "r") as infile:
                for line in infile:
                    line = line.rstrip()
                    line=re.sub(r'<sil[\+\w]*>',r'',line)
                    wordSet.add(line)

    wordSet.remove("")



def generateDictionary():

    wordList = sorted(list(wordSet))

    #wordsStr = "\n".join(wordList)
    #print ">>>> wordsStr\n" + wordsStr


    phonemeSet = set([])

    with open("../target/liepa_zodziai.csv", "a") as outfile:
        for word in wordList:
            outfile.write(word + "\n")

    with open("../target/liepa.dic", "a") as outfile:
        for i in range(len(wordList)):
            key = wordList[i]
            value = transcriber.transcribe(key)
            phonemeSet.update(value.split(" "))
            output = "{}\t{}\n".format(key, value)
            outfile.write(output)


    with open("../target/liepa.phone", "w") as outfile:
        outfile.write("SIL\n")
        #outfile.write("SILPAUSE\n")
        #outfile.write("SILBREIN\n")
        #outfile.write("SILBREOUT\n")
        for phone in sorted(phonemeSet):
            outfile.write(phone + "\n")

if __name__ == "__main__":
    try:
        os.remove("../target/liepa_zodziai.csv")
        os.remove("../target/liepa.dic")
    except OSError:
        pass
    readRepo(test_repo_name)
    readRepo(train_repo_name)
    generateDictionary()
