# -*- coding: utf-8 -*-
import sys
import random
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

    data = fr.read()
    blocks = data.split('<DOCUMENT>\n')

    # get rid of empty doc
    valid_doc = []
    for doc in blocks:
        if doc.strip() != "":
            valid_doc.append(doc)

    # shuffle doc
    random.shuffle(valid_doc)
    fw.write('<DOCUMENT>\n' + '<DOCUMENT>\n'.join(valid_doc))

    fr.close()
    fw.close()
