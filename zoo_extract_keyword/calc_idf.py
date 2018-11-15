#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from math import log
doc_num=float(sys.argv[1])
countdict={}
for line in sys.stdin:
    line=line.strip()
    val=line.split("\t")
    tdict={}
    for sen in val:
        sp=sen.split(" ")
        for word in sp:
            word=word.split(":")[0]
            if(word==""):
                continue
            if(not tdict.has_key(word)):
                tdict[word]=""
                if(countdict.has_key(word)):
                    countdict[word]+=1
                else:
                    countdict[word]=1
for word in countdict:
    print word+"\t"+str(log(doc_num/countdict[word]))
