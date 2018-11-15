# -*- coding: utf-8 -*-
import sys
import codecs
from predict import Seq2SeqPredictor

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python", sys.argv[0], "<input> <count> <output>"
        exit(-1)
    else:
        fn_in = sys.argv[1]
        num = int(sys.argv[2])
        fn_out = sys.argv[3]

    fr = codecs.open(fn_in, 'r', 'utf-8')
    fw = codecs.open(fn_out, 'w', 'utf-8')

    with Seq2SeqPredictor() as predictor:
        for line in fr:
            line = line.strip()

            # topic examples
            # 时尚教主_喜悦   潮人 气派 时尚教主 高兴 为之一喜 欢呼雀跃
            # 时尚教主_喜悦   潮人 兴高彩烈 教主 可贺 惊喜万分 手舞足蹈

            [label, topic] = line.split('\t')
            keywords = topic.split('|')

            # predict poetry lines, totally num poems
            for k in range(0, num):

                # output label and keywords first
                fw.write(label + '\n')
                fw.write("Keywords:[%s]\n" % (' '.join(keywords)))

                # predict poetry
                try:
                    poems = predictor.predict(keywords)
                except Exception:
                    fw.write("Error!\n")
                    exit(-1)

                # add punctuations
                for i in range(0, len(poems)):
                    if i < len(poems) - 1:
                        fw.write(poems[i] + u'，\n')
                    else:
                        fw.write(poems[i] + u'。\n')

                fw.write('\n')

    fr.close()
    fw.close()
