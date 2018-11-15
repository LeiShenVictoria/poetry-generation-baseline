## Requirements ##
tensorflow-gpu 1.3
python 2.7

## Peotry Generation ##
Original code: https://github.com/Disiok/poetry-seq2seq

## How to run it? ##
1) You need to set up your tensorflow develop environment, please refer to: http://cf.jd.com/pages/viewpage.action?pageId=107666568

2) Prepare your corpus, refer to data/train.txt

3) Generate vocab
   python vocab.py

4) Start training
   python train.py

5) Start decoding
   python demo.py   

## Important Updates ##
## 2018-08-06 ##
Support mix-input (word+char), and coverage decoder

## 2018-06-03 ##
Add hyper-parameter length_penalty_weight

## 2018-05-27 ##
Remove useless python files into deprecated directory.

## 2018-05-23 ##
Initialized poetry-generation repository, different from orignal code, we support beam search decoding and also add code to output tensorflow graph for java to call.

