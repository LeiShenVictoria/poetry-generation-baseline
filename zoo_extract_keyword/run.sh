#example for simplified chinese input, which need set ch=true
input="result_all_poem.txt"
#example for english input, which need set ch=false
input="foo.txt"
output="res.txt"
## max char num of keyword
max_keyword_length=20
## max char num of sentence
max_sentence_length=100
## min sentences num of 
min_doc_sentences_num=1
ch=false
## if source language is simplified chinese, Then parallel segment will be used
if ${ch}
then
    #parallel thread num tp segment sentence to word
    total_count=`cat $input|wc -l`
    split_num=20
    line_num=$[$total_count/$split_num]
    ps -ef | grep test | grep batch_segment | awk '{print $2}' | xargs kill
    rm -rf split_*
    split ${input} -d -l ${line_num} split_
    for file in `ls split_*`
    do
        cat $file | python batch_segment.py > ${file}_seg.res &
    done
    wait
    cat split_*.res | python merge_uniq.py 1 > temp.txt
    rm -f split_*
else
    cat ${input} |python merge_uniq.py 0 |tr A-Z a-z > temp.txt
fi
docnum=`cat temp.txt|wc -l`
cat temp.txt|python calc_idf.py ${docnum} >word_idf1.txt
cat temp.txt | python extract_keyword1.py word_idf1.txt ${ch}| python filt_sentence_keyword_length.py ${max_keyword_length} ${max_sentence_length} | python filt_paragraph_length.py ${min_doc_sentences_num} >${output}
