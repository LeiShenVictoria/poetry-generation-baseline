#! /usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from vocab import *

train_path = os.path.join(DATA_DIR, 'train.txt')


def fill_np_matrix(vects, batch_size, value):
    max_len = max(len(vect) for vect in vects)
    res = np.full([batch_size, max_len], value, dtype=np.int32)
    for row, vect in enumerate(vects):
        res[row, :len(vect)] = vect
    return res


def fill_np_array(vect, batch_size, value):
    result = np.full([batch_size], value, dtype=np.int32)
    result[:len(vect)] = vect
    return result


def process_sentence(sentence, rev=False, pad_len=None, pad_token=PAD_TOKEN):
    if rev:
        sentence = sentence[::-1]

    sentence_ints = sentence_to_ints(sentence)

    if pad_len is not None:
        result_len = len(sentence_ints)
        for i in range(pad_len - result_len):
            sentence_ints.append(pad_token)

    return sentence_ints


def prepare_batch_predict_data(keywords, previous=[], prev=True, rev=False, align=False, keep_prev_num=4,
                               sen_pad_len=20, keyword_pad_len=4):
    # previous sentences
    previous_sentences_ints = []
    lp = len(previous)
    if lp > keep_prev_num:
        previous = previous[lp - keep_prev_num:]
    for sentence in previous:
        sentence_ints = process_sentence(sentence.split(), rev=rev, pad_len=sen_pad_len if align else None)
        previous_sentences_ints += [SEP_TOKEN] + sentence_ints

    # allow multi-keywords as input
    keywords_ints = []
    for kw in keywords.split(','):
        kw_ints = process_sentence(kw.split(), rev=rev, pad_len=keyword_pad_len if align else None)
        keywords_ints += [SEP_TOKEN] + kw_ints

    source_ints = keywords_ints + (previous_sentences_ints if prev else [])
    source_len = len(source_ints)

    # print 'keywords_ints', keywords_ints
    # print 'source_ints', source_ints

    source = fill_np_matrix([source_ints], 1, PAD_TOKEN)
    source_len = np.array([source_len])

    return source, source_len


def get_second_sep_token_position(previous_sentences_ints):
    k = 1
    for key in previous_sentences_ints[1:]:
        if key == SEP_TOKEN:
            break
        k += 1
    return k


def gen_batch_train_data(batch_size, prev=True, rev=False, align=False, keep_prev_num=4, sen_pad_len=20,
                         keyword_pad_len=4, train_data_path=train_path):
    """
    Get training data in batch major format, with keyword and previous sentences as source,
    aligned and reversed

    Args:
        batch_size:

    Returns:
        source: [batch_size, time_steps]: keywords + SEP + previous sentences
        source_lens: [batch_size]: length of source
        target: [batch_size, time_steps]: current sentence
        target_lens: [batch_size]: length of target
    """
    poem_sentence_count = 0
    count = 0
    with codecs.open(train_data_path, 'r', 'utf-8') as fin:
        stop = False
        while not stop:
            source = []
            source_lens = []
            target = []
            target_lens = []

            previous_sentences_ints = []
            i = 0
            while i < batch_size:
                line = fin.readline()
                count += 1
                if count % 10000 == 0:
                    print "processed lens ", count
                if not line:
                    stop = True
                    break
                else:
                    line = line.strip()
                    # clear history when one document ends
                    if line == "<DOCUMENT>":
                        previous_sentences_ints = []
                        poem_sentence_count = 0
                        continue

                    # prepare training batch
                    current_sentence, keywords = line.split('\t')
                    current_sentence_ints = process_sentence(current_sentence.split(), rev=rev,
                                                             pad_len=sen_pad_len if align else None)

                    # support multi-keywords as input
                    keywords_ints = []
                    for kw in keywords.split(','):
                        kw_ints = process_sentence(kw.split(), rev=rev,
                                                   pad_len=keyword_pad_len if align else None)
                        keywords_ints += [SEP_TOKEN] + kw_ints

                    source_ints = keywords_ints + (previous_sentences_ints if prev else [])
                    # print 'keywords_ints', keywords_ints
                    # print 'source_ints', source_ints

                    target.append(current_sentence_ints)
                    target_lens.append(len(current_sentence_ints))

                    source.append(source_ints)
                    source_lens.append(len(source_ints))

                    # Always append to previous sentences
                    previous_sentences_ints += [SEP_TOKEN] + current_sentence_ints
                    poem_sentence_count += 1
                    if poem_sentence_count > keep_prev_num:
                        k = get_second_sep_token_position(previous_sentences_ints)
                        # print poem_sentence_count,k
                        previous_sentences_ints = previous_sentences_ints[k:]
                    i += 1

            if len(source) == batch_size:
                source_padded = fill_np_matrix(source, batch_size, PAD_TOKEN)
                target_padded = fill_np_matrix(target, batch_size, PAD_TOKEN)
                source_lens = np.array(source_lens)
                target_lens = np.array(target_lens)

                yield source_padded, source_lens, target_padded, target_lens


if __name__ == '__main__':
    pass
