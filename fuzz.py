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

import sys
import json
import jsonFuzzer

import glob

def usage():
    print "jsonFuzzer Example application"
    print "Usage: fuzz.py <folder>"
    print "\twhere folder contains JSON examples"

def main(argv = sys.argv):

    if(len(argv)<2):
        usage()
        exit(1)

    jf = jsonFuzzer.jsonFuzzer()

    path =  argv[1]+"/*.json"
    for j in glob.glob(path):
        jstream = open (j, "r")
        jo = json.load(jstream)

        jf.putExample(jo)

    jf.PROB_REPLACE=0.5
    jf.PROB_FREESTRING=0.5

    for i in range(10):
        jTest=jf.generateTest()
        print json.dumps(jTest)
        print "\n----\n\n"


if __name__ == "__main__":

    main()
