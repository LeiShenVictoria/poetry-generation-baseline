#!/bin/sh

## set GPU card to use
export CUDA_VISIBLE_DEVICES=0

## prepare training data
#cd step_prep_train_data
#./run.sh

## prepare word embedding
#cd step_prep_word_embedding
#./process.sh

## prepare re-ranking lm
#cd step_train_reranking_lm
#./process.sh

## generate vocab
python vocab.py

## start training
nohup python train.py > log.test.txt &

## try our interactive demo
python demo.py

## generate doc by batch
python batch_gen.py <input> <count> <output>

## for java encapsulation, please refer code in step_java_encapsulation
