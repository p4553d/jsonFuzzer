#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2012, p4553d@googlemail.com

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""


import json
import random
import string
from collections import defaultdict


class jsonFuzzer:

    sourceSet = []
    keySet = []
    valueSet = [""]

    PROB_REPLACE=0.5    # probability for an object to be replaced by another one from the set

    PROB_FREESTRING=0.2
    SPECIAL_CHARS=False      # use of special characters
    MAX_FREESTRING=1024     # max length of self-generated string

    specialChars=u'ÄÖÜäöüß'

    # Populate sets of keys and values with parts of learn set
    def extractParts(self, sub):
        if(isinstance(sub, dict)):
            for key, value in sub.items():
                # collect all strings for key set, plausibiliy check
                if (isinstance(key,basestring)):
                    self.keySet.append(key)
                self.extractParts(value)

        if(isinstance(sub, list)):
            for value in sub:
                self.extractParts(value)

        # it is part of input, good enough for value list
        self.valueSet.append(sub)
        return

    def putExample(self, example):
        if (isinstance(example, dict)==False):
            raise WrongType

        # Extract keys and values
        self.extractParts(example)

        # Store as example
        self.sourceSet.append(example)
        return

    def sloppyKey(self, key):
        if(random.random()>self.PROB_REPLACE):
            retKey=key
        else:
            if(random.random()<self.PROB_FREESTRING):
                retKey=self.generateString()
            else:
                retKey=self.keySet[random.randint(0, len(self.keySet)-1)]
        return retKey

    def sloppyValue(self, value):
        if(random.random()>self.PROB_REPLACE):
            retValue=value
        else:
            if(random.random()<self.PROB_FREESTRING):
                retValue=self.generateString()
            else:
                retValue=self.valueSet[random.randint(0, len(self.valueSet)-1)]
        return retValue

    def generateString(self):
        genStr = string.printable

        if(self.SPECIAL_CHARS==True):
            genStr = genStr + self.specialChars

        ret = u''
        for i in range(random.randint(0,self.MAX_FREESTRING)):
            ret = ret + random.choice(genStr)
        return ret

    def sloppyCopy(self, source):
        target = u''
        if(isinstance(source, dict)):
            target={}
            for key, value in source.items():
                z = self.sloppyCopy(value)
                target[self.sloppyKey(key)] = z
        else:
            if(isinstance(source, list)):
                target=[]
                for value in source:
                    z = self.sloppyCopy(value)
                    target.append(z)
            else:
                target = self.sloppyValue(source)
        return target

    def generateTest(self):
        # pick a random source test
        r = random.randint(0,len(self.sourceSet)-1)
        srcTest = self.sourceSet[r]

        # make deep-copy and mutate
        retTest = self.sloppyCopy(srcTest)
        return retTest

