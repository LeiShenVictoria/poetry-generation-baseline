#! /usr/bin/env python
# -*- coding:utf-8 -*-

from predict import Seq2SeqPredictor


def main():
    with Seq2SeqPredictor() as predictor:
        # Run loop
        terminate = False
        while not terminate:
            try:
                input = raw_input('Input Text, use | to separate keywords: \n').decode('utf-8').strip()

                if not input:
                    print 'Input cannot be empty!'
                elif input.lower() in ['quit', 'exit']:
                    terminate = True
                else:
                    # Generate poems
                    keywords = input.split('|')
                    lines = predictor.predict(keywords)

                    # Print keywords and poems
                    print 'Keyword:\tSentence:'
                    for line_number in xrange(len(lines)):
                        punctuation = u'，'
                        if line_number == len(lines) - 1:
                            punctuation = u'。'
                        print u'{keyword}\t{line}{punctuation}'.format(keyword=keywords[line_number], line=lines[line_number],
                            punctuation=punctuation)

            except EOFError:
                terminate = True
            except KeyboardInterrupt:
                terminate = True

    print '\nTerminated.'


if __name__ == '__main__':
    main()
