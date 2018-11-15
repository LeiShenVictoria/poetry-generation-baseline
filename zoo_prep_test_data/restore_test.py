# -*- coding: utf-8 -*-
import sys
import re
import codecs

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python", sys.argv[0], "<input> <output>"
        exit(-1)
    else:
        fn_in = sys.argv[1]
        fn_out = sys.argv[2]

    fr = codecs.open(fn_in, 'r', 'utf-8')
    fw = codecs.open(fn_out, 'w', 'utf-8')

    for line in fr:
        line = line.strip()
        parts = line.split('|')
        tokens = []
        for keywords in parts:
            kws = keywords.split(',')
            kws = [kw.strip() for kw in kws]
            tokens.append(','.join(kws))
        fw.write('|'.join(tokens) + '\n')

    fr.close()
    fw.close()
