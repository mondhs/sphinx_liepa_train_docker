#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''

import unittest, sys, os
sys.path.insert(0, os.getcwd())
import transcriber_re
# import transcriber_pk


class Test(unittest.TestCase):


    def setUp(self):
        pass

    def test_Regexp(self):
        transcriber = transcriber_re.TranscriberRegexp()

        wordToPhonemeMap = {
            #special symbols
            "laikas" : "L A I K A S",
            "Labas" : "L A B A S",
            "žėlė": "Z2 E3_ L E3_",
            "žvėrelio": "Z2 V E3_ R E L IO_",
        }
        for key, value in wordToPhonemeMap.items():
            phonemeSequence = transcriber.transcribe(key)
            self.assertEqual(value, phonemeSequence)

    # def test_Pijaus(self):
    #     transcriber = transcriber_pk.TranscriberPijaus()
    #
    #     wordToPhonemeMap = {
    #         #special symbols
    #         "laikas" : "l a1 j1 k a s",
    #         "Labas" : "l aa1 b a s",
    #         "žėlė": "z1 e1e l ee",
    #         "žvėrelio": "z1 v ee r ea1 l oo",
    #     }
    #
    #     wordsToPhonemeMap = """laikas
    #          Labas
    #          žėlė
    #          žvėrelio"""
    #
    #     transcribedList = transcriber.transcribe(wordsToPhonemeMap).split("\n")
    #
    #     for transcribedEntry in transcribedList:
    #         [key,value] = transcribedEntry.split("\t")
    #         print [key,value]
    #         self.assertEqual(wordToPhonemeMap[key],value)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
