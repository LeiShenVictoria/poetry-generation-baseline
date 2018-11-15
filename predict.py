#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import json
import re
import tensorflow as tf
from tensorflow.python.framework import graph_util
from data_utils import prepare_batch_predict_data
from model import Seq2SeqModel
from vocab import ints_to_sentence, get_vocab_size
from random import randint

sys.path.append(os.getcwd() + '/zoo_train_reranking_lm/srilm/')
from srilm import *

# Load hyper-parameters
tf.app.flags.DEFINE_boolean('rev_data', True, 'Use reversed training data')
tf.app.flags.DEFINE_boolean('align_data', False, 'Use aligned training data, pad input sentence')
tf.app.flags.DEFINE_boolean('prev_data', True, 'Use training data with previous sentences')
tf.app.flags.DEFINE_boolean('lm_ranking', False, 'Use lm model for ranking generated sentences')
tf.app.flags.DEFINE_string('lm', 'zoo_train_reranking_lm/3gram.lm', 'path for re-ranking language model')
tf.app.flags.DEFINE_integer('ngram', 3, 'Order for language model')
tf.app.flags.DEFINE_integer('keep_prev_num', 2, 'Number of keep previous sentences')
tf.app.flags.DEFINE_integer('sen_pad_len', 15, 'Number of sentence pad length')
tf.app.flags.DEFINE_integer('keyword_pad_len', 4, 'Number of keyword pad length')
tf.app.flags.DEFINE_integer('unique_ratio', 0.5, 'Threshold for unique word ratio')
tf.app.flags.DEFINE_integer('least_length', 4, 'Threshold for sentence length')
tf.app.flags.DEFINE_integer('beam_width', 10, 'Beam width used in beam search decoding')
tf.app.flags.DEFINE_integer('decode_batch_size', 1, 'Batch size used for decoding')
tf.app.flags.DEFINE_integer('max_decode_step', 25, 'Maximum time step limit to decode')
tf.app.flags.DEFINE_boolean('write_n_best', False, 'Write n-best list (n=beam_width)')
tf.app.flags.DEFINE_string('model_path', None, 'Path to a specific model checkpoint.')
tf.app.flags.DEFINE_string('model_dir', 'model', 'Path to load model checkpoints')
tf.app.flags.DEFINE_string('predict_mode', 'greedy', 'Greedy Decoder, activate by set beam width = 1')
tf.app.flags.DEFINE_boolean('allow_soft_placement', True, 'Allow device soft placement')
tf.app.flags.DEFINE_boolean('log_device_placement', False, 'Log placement of ops on devices')

FLAGS = tf.app.flags.FLAGS


# json loads strings as unicode; we currently still work with Python 2 strings, and need conversion
def unicode_to_utf8(d):
    return dict((key.encode("UTF-8"), value) for (key, value) in d.items())


def load_config(FLAGS):
    if FLAGS.model_path is not None:
        checkpoint_path = FLAGS.model_path
        print 'Model path specified at: {}'.format(checkpoint_path)
    elif FLAGS.model_dir is not None:
        checkpoint_path = tf.train.latest_checkpoint(FLAGS.model_dir + '/')
        print 'Model dir specified, using the latest checkpoint at: {}'.format(checkpoint_path)
    else:
        checkpoint_path = tf.train.latest_checkpoint('model/')
        print 'Model path not specified, using the latest checkpoint at: {}'.format(checkpoint_path)

    FLAGS.model_path = checkpoint_path

    # when loading multi-gpu trained model
    # config_unicode = json.load(open(FLAGS.model_dir + "/flags.json", 'rb'))

    # when loading single-gpu trained model
    config_unicode = json.load(open('%s.json' % FLAGS.model_path, 'rb'))
    config = unicode_to_utf8(config_unicode)

    # Overwrite flags
    for key, value in FLAGS.__flags.items():
        config[key] = value

    return config


def load_model(session, model, saver):
    if tf.train.checkpoint_exists(FLAGS.model_path):
        print 'Reloading model parameters..'
        model.restore(session, saver, FLAGS.model_path)
    else:
        raise ValueError('No such file:[{}]'.format(FLAGS.model_path))
    return model


class Seq2SeqPredictor:
    def __init__(self):

        # Load model config
        config = load_config(FLAGS)
        config_proto = tf.ConfigProto(allow_soft_placement=FLAGS.allow_soft_placement,
                                      log_device_placement=FLAGS.log_device_placement,
                                      gpu_options=tf.GPUOptions(allow_growth=True))

        # load LM for re-ranking
        self.re_ranking = FLAGS.lm_ranking
        if self.re_ranking:
            self.load_lm_model()

        self.sess = tf.Session(config=config_proto)

        # create seq2seq model instance
        self.model = Seq2SeqModel(config, 'predict')

        # Create saver
        # Using var_list = None returns the list of all savable variables
        saver = tf.train.Saver(var_list=None)

        # Reload existing checkpoint
        load_model(self.sess, self.model, saver)

    def __enter__(self):
        return self

    def load_lm_model(self):
        language_model = FLAGS.lm
        self.ngram = FLAGS.ngram
        self.n = initLM(self.ngram)
        readLM(self.n, language_model)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sess.close()

    def evaluator(self, sent_list, n):
        score = []

        for utt in sent_list:
            word_list = utt.split()
            sen_len = len(word_list)
            u_sen = utt.encode('utf-8')
            ppl = getSentencePpl(n, str(u_sen), sen_len)
            score.append(ppl)

        sort_index = sorted(range(len(score)), key=lambda k: score[k])
        sorted_list = []

        for i in sort_index:
            utt_no_space = re.sub(' ', '', sent_list[i])
            if self.calc_unique_word_ratio(sent_list[i]) >= FLAGS.unique_ratio and len(
                    utt_no_space) >= FLAGS.least_length:
                sorted_list.append(sent_list[i])

        if len(sorted_list) > 0:
            return sorted_list
        else:
            return [sent_list[sort_index[0]]]

    def calc_unique_word_ratio(self, utt):
        # reject empty sentence
        if utt == "": return 0
        word_set = set()
        for tok in utt.split():
            word_set.add(tok)
        uniq_ratio = float(len(word_set)) / len(utt.split())
        return uniq_ratio

    def predict(self, keywords):
        sentences = []
        sentences_no_space = []
        for keyword in keywords:
            source, source_len = prepare_batch_predict_data(keyword, previous=sentences, prev=FLAGS.prev_data,
                                                            rev=FLAGS.rev_data, align=FLAGS.align_data,
                                                            keep_prev_num=FLAGS.keep_prev_num,
                                                            sen_pad_len=FLAGS.sen_pad_len,
                                                            keyword_pad_len=FLAGS.keyword_pad_len)

            # print 'source: ', source
            # print 'source_len: ', source_len
            predicted_batch = self.model.predict(self.sess, encoder_inputs=source, encoder_inputs_length=source_len)

            # added by lrx, store model in binary format, so Java can call it
            # tensor_names = [t.name for op in tf.get_default_graph().get_operations() for t in op.values()]
            # for i in tensor_names: print i
            # output_graph_def = tf.graph_util.convert_variables_to_constants(self.sess, self.sess.graph_def, output_node_names=['seq2seq/decoder/out_put0000'])
            # tf.train.write_graph(output_graph_def, FLAGS.model_dir, 'minimal_graph.proto', as_text=False)

            # parse decoding results
            if FLAGS.beam_width > 1:
                predicted_line = predicted_batch[0]
                # print predicted_line
                sent_set = []

                for i in range(FLAGS.beam_width):
                    predicted_ints = []
                    for j in range(len(predicted_line)):
                        if predicted_line[j][i] == get_vocab_size() - 2:
                            break
                        else:
                            predicted_ints.append(predicted_line[j][i])

                    # reverse first, then map ints to words
                    if FLAGS.rev_data:
                        predicted_ints = predicted_ints[::-1]

                    predicted_sentence = ints_to_sentence(predicted_ints)
                    sent_set.append(predicted_sentence)

                # load LM to re-rank all candidates
                if self.re_ranking:
                    sent_set = self.evaluator(sent_set, self.n)
                    idx = 0
                    if len(sent_set) > 1:
                        idx = randint(0, len(sent_set) - 2)
                else:
                    idx = randint(0, len(sent_set) - 1)

                # output all candidates
                # all_sents = '|'.join(sent_set)
                # print all_sents
                sentences.append(sent_set[idx])

            else:
                predicted_line = predicted_batch[0]  # predicted is a batch of one line
                predicted_line_clean = predicted_line[:-1]  # remove the end token
                predicted_ints = map(lambda x: x[0], predicted_line_clean)  # Flatten from [time_step, 1] to [time_step]

                if FLAGS.rev_data:
                    predicted_ints = predicted_ints[::-1]

                predicted_sentence = ints_to_sentence(predicted_ints)
                sentences.append(predicted_sentence)

        # remove space
        for s in sentences:
            s = re.sub(' ', '', s)
            sentences_no_space.append(s)

        return sentences_no_space


def main(_):
    KEYWORDS = [u'妈妈,生日,健康,感谢,快乐', u'妈妈,生日,健康,感谢,快乐', u'妈妈,生日,健康,感谢,快乐', u'妈妈,生日,健康,感谢,快乐', u'妈妈,生日,健康,感谢,快乐']
    with Seq2SeqPredictor() as predictor:
        lines = predictor.predict(KEYWORDS)
        for line in lines:
            print line


if __name__ == '__main__':
    tf.app.run()
