#! /usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import os,sys
from gensim.models.keyedvectors import KeyedVectors
model=KeyedVectors.load_word2vec_format("data/word2vec.txt", binary=False,unicode_errors='ignore')
word_list={}
dim=0
for line in open("data/word2vec.txt"):
    line=line.strip().decode("utf8")
    val=line.split(" ")
    if(len(val)==2):
        dim=int(val[1])
        continue
    word_list[val[0]]=""
keyword_count={}
for line in open("data/train.txt"):
    line=line.strip()
    val=line.split("\t")
    lval=len(val)
    if(lval!=2):
        continue
    sp=val[1].split(",")
    for word in sp:
        if(keyword_count.has_key(word)):
            keyword_count[word.decode("utf8")]+=1
        else:
            keyword_count[word.decode("utf8")]=1

def expand_keyword(keyword_list=None, min_keywords_count=5, expand_num=5):
    res=model.most_similar(positive=keyword_list, topn =expand_num*10)
    ret=[]
    for key in res:
        if(keyword_count.has_key(key[0])):
            ret.append(key[0])
    if(len(ret)>=expand_num):
        ret=ret[0:expand_num]
    return ret
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage: python", sys.argv[0], "<input> <min_keywords_count> <expand_num> <output>"
        exit(-1)
    else:
        fn_in = sys.argv[1]
        min_keywords_count = int(sys.argv[2])
        expand_num = int(sys.argv[3])
        fn_out = sys.argv[4]
    keyword_list=[]
    res=[]
    for line in open(fn_in):
        line=line.strip().decode("utf8")
        if(keyword_count.has_key(line)):
            keyword_list.append(line)
            res.append(line)
        elif(word_list.has_key(line)):
            keyword_list.append(line)
    if(len(keyword_list)>0):
        ret=expand_keyword(keyword_list=keyword_list, min_keywords_count=min_keywords_count, expand_num=expand_num)
        res.extend(ret)
        res=map(lambda x:x.encode("utf8"),res)
        fd=open(fn_out,"w")
        fd.write("\n".join(res)+"\n")
    else:
        print "all inputword is oov"
