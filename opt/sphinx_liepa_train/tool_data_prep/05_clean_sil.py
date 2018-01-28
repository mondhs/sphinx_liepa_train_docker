#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import  re

silTransfomration = [
    ("<sil[\+\w]+>", "<sil>")

]

train_repo_name="train"
test_repo_name="test"


def processRepo(repo_name):
    with open('../target/liepa_'+repo_name+'_sil.transcription', 'r') as input_file, open('../target/liepa_'+repo_name+'.transcription', 'w') as output_file:
        for line in input_file:
            #line = line.decode("utf-8")
            line=re.sub(r'<sil[\+\w]+>',r'<sil>',line)
            line=re.sub(r'<s> *<sil>',r'<s>',line)
            line=re.sub(r'<sil> *</s>',r'</s>',line)
            line=re.sub(r'( *<sil>)+',r' <sil>',line)
            output_file.write(line )


if __name__ == "__main__":
    processRepo(test_repo_name)
    processRepo(train_repo_name)
