#!/bin/sh

work=tmp
mkdir -p $work

data=test.blessings.txt
vocab=../zoo_prep_train_data/tmp/vocab.top50k.xdb

## word segmentation
cat $data | awk -F'\t' '{print $2}' | perl -pe 's/ /|/g' > $work/test.kw.unseg
scws -i $work/test.kw.unseg -c utf8 -d $vocab -o $work/test.kw.seg
python restore_test.py $work/test.kw.seg $work/test.kw.txt

## add back doc id
awk -F'\t' '{print $1}' $data > $work/test.id.txt
paste $work/test.id.txt $work/test.kw.txt > test.input.txt

