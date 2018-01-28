#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''

import unittest, sys, os
sys.path.insert(0, os.getcwd())
import transcriber_re


class Test(unittest.TestCase):


    def setUp(self):
        pass

    def test_Regexp(self):
        transcriber = transcriber_re.TranscriberRegexp()

        wordToPhonemeMap = {
            #special symbols
            "Labas" : "L A B A S",
            "žėlė": "Z2 E3_ L E3_",
            "žvėrelio": "Z2 V E3_ R E L IO_",
        }
        for key, value in wordToPhonemeMap.items():
            phonemeSequence = transcriber.transcribe(key)
            self.assertEqual(value, phonemeSequence)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
