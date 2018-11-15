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
        parts = line.split('\t')
        if len(parts) == 3:
            toks = parts[1].split()
            word_set = []
            for w in toks:
                [word, pos, weight] = w.split(':')
                word_set.append(word)
            fw.write(parts[0] + '\t' + ' '.join(word_set) + '\t' + parts[2] + '\n')
        else:
            fw.write(line + '\n')

    fr.close()
    fw.close()