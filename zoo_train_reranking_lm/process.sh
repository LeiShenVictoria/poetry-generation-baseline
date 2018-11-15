#!/bin/sh

work=tmp
mkdir -p $work

## if word-based, train 3gram, if char-based, train 5gram
cat ../data/train.txt | grep -v "<DOCUMENT>" | awk -F'\t' '{if(NF==2)print $1}' > $work/corpus.txt
ngram-count -text $work/corpus.txt -lm $work/3gram.lm -order 3 -kndiscount -write-binary-lm

rm -rf $work
