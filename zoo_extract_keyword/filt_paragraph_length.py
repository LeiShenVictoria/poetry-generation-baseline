#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,copy
tlist=[]
tdict={}
length=int(sys.argv[1])
fd=open("filt.log","w")
for line in sys.stdin:
    line=line.strip()
    if(line.startswith("<")):
        if(len(tlist)>length):
             tdict["\n".join(tlist)]=""
        else:
            fd.write("\n".join(tlist)+"\n")
        tlist=[]
        tlist.append("<DOCUMENT>")
        continue
    tlist.append(line)
if(len(tlist)>length):
    tdict["\n".join(tlist)]=""
for key in tdict:
    print key
        
