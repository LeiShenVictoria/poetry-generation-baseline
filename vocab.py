#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import codecs

VOCAB_SIZE = 50000
SEP_TOKEN = 0
PAD_TOKEN = VOCAB_SIZE - 2
DATA_DIR = 'data'
MODEL_DIR = 'model'
LOG_DIR = 'log'

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

vocab_path = os.path.join(DATA_DIR, 'vocab.txt')
corpus_path = os.path.join(DATA_DIR, 'train.txt')


def gen_vocab():

    print("Generating the vocabulary ...")
    vocab_dict = {}

    with codecs.open(corpus_path, 'r', 'utf-8') as fr:
        for line in fr:
            line = line.strip()
            if line == '<DOCUMENT>': continue
            [sentence, keyword] = line.split('\t')

            # count word frequency
            for w in sentence.split():
                if vocab_dict.has_key(w):
                    vocab_dict[w] += 1
                else:
                    vocab_dict[w] = 1

            # put all keywords into vocab, and promote them
            for kw in keyword.split(","):
                for w in kw.split():
                    if vocab_dict.has_key(w):
                        vocab_dict[w] += 20
                    else:
                        vocab_dict[w] = 20

        # sort vocab by frequency
        sort_vocab = sorted(vocab_dict.items(), key=lambda k: k[1], reverse=True)
        vocab_size = len(sort_vocab)
        if vocab_size > VOCAB_SIZE: vocab_size = VOCAB_SIZE
        vocab = [k for (k, v) in sort_vocab][:vocab_size - 3]

    # output vocab into json file
    with codecs.open(vocab_path, 'w', 'utf-8') as fw:
        fw.write('\n'.join(vocab) + '\n')

    print("Total %s words are selected into vocab" % len(vocab))


def get_vocab():
    """Get index2char mapping and char2index mapping from generated json file.
    If the dictionary json does not exist, generate a new dictionary."""

    if not os.path.exists(vocab_path):
        gen_vocab()

    int2ch = [u'<START>']
    with codecs.open(vocab_path, 'r', 'utf-8') as fin:
        for line in fin:
            line = line.strip()
            int2ch.append(line.strip())
    int2ch.append(u'<PAD>')
    int2ch.append(u'<UNK>')

    ch2int = dict((ch, idx) for idx, ch in enumerate(int2ch))
    return int2ch, ch2int


def get_vocab_size():
    return len(int2ch)


# get mapping table
int2ch, ch2int = get_vocab()


def int_to_ch(i):
    return int2ch[i]


def ch_to_int(ch):
    if ch2int.has_key(ch):
        return ch2int[ch]
    else:
        return len(ch2int) - 1


def sentence_to_ints(sentence):
    return map(ch_to_int, sentence)


def ints_to_sentence(ints):
    return ' '.join(map(int_to_ch, ints))


def main():
    int2ch, _ = get_vocab()
    print("Size of the vocabulary: {}".format(len(int2ch)))
    print("Top 100 words:")
    print(', '.join(int2ch[:100]))


if __name__ == '__main__':
    main()
