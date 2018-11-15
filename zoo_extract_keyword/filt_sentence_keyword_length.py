#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
keyword_length=int(sys.argv[1])
sentence_length=int(sys.argv[2])
for line in sys.stdin:
    line=line.strip()
    val=line.split("\t")
    if(line.startswith("<")):
        print "<DOCUMENT>"
        continue
    if(len(val[2].decode("utf8"))>keyword_length or len(val[0].replace(" ","").decode("utf8"))>sentence_length):
        continue
    print line
        
