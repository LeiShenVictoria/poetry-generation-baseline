#!/usr/bin/python 
# -*- coding: utf-8 -*-
import sys
tdict={}
tlist=[]
num=int(sys.argv[1])
val_num=num+1
for line in sys.stdin:
	line=line.strip()
	val=line.split("\t")
	if(len(val)!=val_num):
		continue
	if(line.startswith("<")):
		if(len(tlist)>=1):
			tdict["\t".join(tlist)]=""
		tlist=[]
		continue
	tlist.append(val[num])
if(len(tlist)>=0):
	tdict["\t".join(tlist)]=""
for key in tdict:
	print key
