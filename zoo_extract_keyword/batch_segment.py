# encoding=utf-8
import jieba,sys
import jieba.posseg as pseg
jieba.load_userdict("customer_word.dat")
skip_flag="T"
for line in sys.stdin:
	line = line.strip()
	res=pseg.cut(line)
	res1=map(lambda (word,flag):word.encode("utf8")+":"+str(flag),res)
	print line+"\t"+" ".join(res1)
