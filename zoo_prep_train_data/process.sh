#!/bin/sh

work=tmp
mkdir -p $work

## input corpus
#data=/export/scratch/chenmeng/dataset/poetry_generation/training/blessings/train.blessings.v2.txt
cat train.lyrics+poems.v3.txt train.blessings.v2.txt > $work/training.all.txt
data=$work/training.all.txt

## 1. prepare char-based training data
#python prep_char_train_data.py $data train.char.txt


## 2. prepare word-based training data
# get top 50k vocab
python select_seg_text.py $data $work/data.orig.seg
cat $work/data.orig.seg | awk -F'\t' '{if(NF==3)print $2}' > $work/data.orig.seg.clean
ngram-count -text $work/data.orig.seg.clean -write-order 1 | sort -k2,2 -rg > $work/unigram.txt
cat $work/unigram.txt | awk -F'\t' '{print $1}' | head -n 50000 > $work/vocab.top50k

# re-segment corpus
scws-gen-dict -i $work/vocab.top50k -o $work/vocab.top50k.xdb -c utf8
python prep_unseg_corpus.py $work/data.orig.seg $work/data.unseg
scws -i $work/data.unseg -c utf8 -d $work/vocab.top50k.xdb -o $work/data.seg
python restore_data.py $work/data.seg $work/train.word.txt

# shuffle corpus
python shuffle_corpus.py $work/train.word.txt train.word.txt

# delete tmp files
#rm -rf $work

