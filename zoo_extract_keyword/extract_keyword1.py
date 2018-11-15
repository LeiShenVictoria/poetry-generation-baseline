#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
fd=open(sys.argv[1])
segment=sys.argv[2]
idf={}
punc_list=['n','a']
for line in fd:
    line=line.strip()
    val=line.split("\t")
    if(len(val)!=2):
        continue
    idf[val[0]]=float(val[1])
def extract_keyword_by_pos(val,tf_idf_dict):
    for sen in val:
        tdict={}
        naflag=False
        vflag=False
        lengthflag=False
        sp=sen.split(" ")
        for word in sp:
            w=word.split(":")[0]
            p=word.split(":")[1]
            tdict[word]=tf_idf_dict[w]
            if(p in punc_list and len(w.decode("utf8"))>=2):
                naflag=True
            if(p == 'v' and len(w.decode("utf8"))>=2):
                vflag=True
            if(len(w.decode("utf8"))>=2):
                lengthflag=True
        sorted_list = sorted(tdict.items(), key=lambda d: d[1], reverse=True)
        sen=" ".join([word+":"+str(tf_idf_dict[word.split(":")[0]]) for word in sen.split(" ")])
        sen1="".join([word.split(":")[0] for word in sen.split(" ")])
        if naflag:
            for item in sorted_list:
                sp=item[0].split(":")
                w=sp[0]
                p=sp[1]
                if(p in punc_list and len(w.decode("utf8"))>=2):
                    print sen1+"\t"+sen+"\t"+w
                    break
        elif vflag:
            for item in sorted_list:
                sp=item[0].split(":")
                w=sp[0]
                p=sp[1]
                if(p == 'v' and len(w.decode("utf8"))>=2):
                    print sen1+"\t"+sen+"\t"+w
                    break
        elif lengthflag:
            for item in sorted_list:
                sp=item[0].split(":")
                w=sp[0]
                if(len(w.decode("utf8"))>=2):
                    print sen1+"\t"+sen+"\t"+w
                    break
        else:
            print sen1+"\t"+sen+"\t"+sorted_list[0][0].split(":")[0]

            
def extract_keyword(val,tf_idf_dict):
    for sen in val:
        tdict={}
        sp=sen.split(" ")
        for word in sp:
            tdict[word]=tf_idf_dict[word]
        sorted_list = sorted(tdict.items(), key=lambda d: d[1], reverse=True)
        sen1=" ".join([word+":"+str(tf_idf_dict[word.split(":")[0]]) for word in sen.split(" ")])
        print sen+"\t"+sen1+"\t"+sorted_list[0][0]
for line in sys.stdin:
    print "<DOCUMENT>"
    line=line.strip()
    val=line.split("\t")
    tf_idf_dict={}
    total_count=0
    for sen in val:
        sp=sen.split(" ")
        lsp=len(sp)
        total_count+=lsp
        for word in sp:
            w=word.split(":")[0]
            if(tf_idf_dict.has_key(w)):
                tf_idf_dict[w]+=1.0
            else:
                tf_idf_dict[w]=1.0
    for w in tf_idf_dict:
        tf_idf_dict[w]/=total_count
        tf_idf_dict[w]*=idf[w]
    if segment!="false":
        extract_keyword_by_pos(val,tf_idf_dict)
    else:
        extract_keyword(val,tf_idf_dict)
        
    
            
        
