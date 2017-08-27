#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import  re

silTransfomration = [
    ("<sil[\+\w]+>", "<sil>")
    
]


def multiple_replace(text):
    #print "["+text+"]"
    keys = map(lambda x: x[0], silTransfomration)
    rulesDict = dict(silTransfomration)
    regexStr = "(%s)" % "|".join(map(re.escape, keys))
    # Create a regular expression  from the dictionary keys
    regex = re.compile(regexStr)
    return regex.sub(lambda mo: " " + rulesDict[mo.string[mo.start():mo.end()]] + " ", text)
    
    
with open('../target/liepa_train_sil.transcription', 'r') as input_file, open('../target/liepa_train.transcription', 'w') as output_file:
    for line in input_file:
        line = line.decode("utf-8")
        line=re.sub(r'<sil[\+\w]+>',r'<sil>',line)
        line=re.sub(r'<s> *<sil>',r'<s>',line)
        line=re.sub(r'<sil> *</s>',r'</s>',line)
        line=re.sub(r'( *<sil>)+',r' <sil>',line)
        output_file.write(line.encode("utf-8") )
