#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import numpy as np
from vocab import *
from numpy.random import uniform

_w2v_path = os.path.join(DATA_DIR, 'word2vec.npy')
pretrain_w2v_path = os.path.join(DATA_DIR, 'word2vec.txt')


def _gen_embedding(ndim):
    print "Generating %d-dim word embedding ..." % ndim
    int2ch, ch2int = get_vocab()
    print "vocab size is: " + str(len(int2ch))

    w2v = dict()
    fd = open(pretrain_w2v_path)
    for line in fd:
        line = line.strip()
        val = line.split(" ")
        if len(val) != ndim + 1:
            continue
        w2v[val[0].decode("utf8")] = map(lambda x: float(x), val[1:])

    embedding = uniform(-1.0, 1.0, [get_vocab_size(), ndim])
    for idx, ch in enumerate(int2ch):
        if ch in w2v:
            embedding[idx, :] = np.array(w2v[ch])
    np.save(_w2v_path, embedding)
    print "Word embedding is saved."


def get_word_embedding(ndim):
    if not os.path.exists(_w2v_path):
        _gen_embedding(ndim)
    return np.load(_w2v_path)

