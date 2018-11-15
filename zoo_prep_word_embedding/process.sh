#!/bin/sh

work=tmp
mkdir -p $work

## compile tools
#g++ word2vec_sse.c -o word2vec_sse -lpthread -O3

## prepare training data
data=../step_prep_train_data/train.word.txt
cat $data | grep -v "<DOCUMENT>" | awk -F'\t' '{print $1}' > $work/train.w2v.txt

## train word embedding
./word2vec_sse -train $work/train.w2v.txt \
-output word2vec.txt \
-cbow 0 \
-size 128 \
-window 5 \
-negative 5 \
-hs 1 \
-sample 1e-3 \
-threads 40 \
-binary 0 \
-iter 20 \
-min-count 1

## delete tmp files
rm -rf $work

