package com.jd.jnlu.nlg.model;

import com.google.common.base.Preconditions;
import com.google.common.collect.Maps;
import com.google.common.io.Closeables;
import com.google.common.primitives.Ints;
import edu.stanford.nlp.io.IOUtils;
import org.assertj.core.util.Lists;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;

public final class DataPreprocessorImpl implements DataPreprocessor {
    //private static final Logger LOGGER = LoggerFactory.getLogger(DataPreprocessorImpl.class);

    private final Map<String, Integer> vocabularyIndexMap;
    private final Map<Integer, String> IndexVocaMap;
    private final int unkIndex;

    private final int VOCAB_SIZE = 10600;
    private final int SEP_TOKEN = 0;
    private final int PAD_TOKEN = 10599;

    public DataPreprocessorImpl(String vocabPath) throws IOException {
        Preconditions.checkNotNull(vocabPath);

        this.vocabularyIndexMap = loadData(vocabPath);
        this.IndexVocaMap = loadChas(vocabPath);

        Integer unknownIndex = this.vocabularyIndexMap.get("<UNK>");
        if (unknownIndex == null) {
            this.unkIndex = PAD_TOKEN + 1;
        } else {
            this.unkIndex = unknownIndex;
        }

        //LOGGER.info("Created DataPreprocessor! unk_index={}", unkIndex);
    }

    private List<Integer> PadList(List<Integer> oldList, int length, int pad) {
        if (oldList.size() >= length) {
            return oldList.subList(0, length + 1);
        } else {

            for (int i = oldList.size(); i < length; i++)
                oldList.add(pad);
            return oldList;
        }

    }

    private Map<String, Integer> loadData(String dataPath) throws IOException {
        Map<String, Integer> map = Maps.newHashMap();
        BufferedReader bufferedReader = IOUtils.readerFromString(dataPath);
        try {
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) {
                    //LOGGER.warn("Empty line!");
                    continue;
                }
                String[] strs = line.split("\t");
                if (strs.length != 2) {
                    //LOGGER.warn("Invalid line: " + line);
                    continue;
                }
                String key = strs[0];

                int index;
                try {
                    index = Integer.parseInt(strs[1]);
                } catch (NumberFormatException e) {
                    //LOGGER.warn("Invalid line: " + line, e);
                    continue;
                }

                map.put(key, index);
            }
        } finally {
            Closeables.closeQuietly(bufferedReader);
        }
        return map;
    }

    private Map<Integer, String> loadChas(String dataPath) throws IOException {
        Map<Integer, String> map = Maps.newHashMap();
        BufferedReader bufferedReader = IOUtils.readerFromString(dataPath);
        try {
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) {
                    //LOGGER.warn("Empty line!");
                    continue;
                }
                String[] strs = line.split("\t");
                if (strs.length != 2) {
                    //LOGGER.warn("Invalid line: " + line);
                    continue;
                }
                String key = strs[0];

                int index;
                try {
                    index = Integer.parseInt(strs[1]);
                } catch (NumberFormatException e) {
                    //LOGGER.warn("Invalid line: " + line, e);
                    continue;
                }

                map.put(index, key);
            }
        } finally {
            Closeables.closeQuietly(bufferedReader);
        }
        return map;
    }


    public DataEntry preprocess(List<List<String>> keywords, List<List<String>> previous, Boolean reverse) {

        // previous sentences
        if(reverse){
            for(List<String> sent : previous){
                Collections.reverse(sent);
            }
        }
        List<Integer> previousSentencesInts = Lists.newArrayList();
        for (List<String> sentence : previous) {

            List<Integer> sentInts = SentenceToInts(sentence);

//            sentInts = PadList(sentInts, 20, PAD_TOKEN);
            previousSentencesInts.add(SEP_TOKEN);
            previousSentencesInts.addAll(sentInts);
        }

        //keywords
        if (reverse) {
            for(List<String> keyword : keywords){
                Collections.reverse(keyword);
            }
        }

        List<Integer> keywordsints = Lists.newArrayList();
        for(List<String> keyword : keywords){
            List<Integer> keywordints = Lists.newArrayList();
            for (String kw : keyword) {
                Integer keywordInts = CharToInt(kw);

                keywordints.add(keywordInts);
            }

//            keywordints = PadList(keywordints, 6, PAD_TOKEN);
            keywordsints.add(SEP_TOKEN);
            keywordsints.addAll(keywordints);
        }

        keywordsints = keywordsints.subList(1, keywordsints.size());

        List<Integer> sourceInts = Lists.newArrayList();
        sourceInts.addAll(keywordsints);
        sourceInts.addAll(previousSentencesInts);
        List<Integer> sourceLength = Lists.newArrayList();
        sourceLength.add(sourceInts.size());
        int[] source = Ints.toArray(sourceInts);
        int[] sourceLen = Ints.toArray(sourceLength);
        return new DataEntry(source, sourceLen);
    }

    private List<Integer> SentenceToInts(List<String> sentence) {
        Preconditions.checkNotNull(sentence);
        List<Integer> sentInts = Lists.newArrayList();
        for (String word : sentence) {

            sentInts.add(CharToInt(word));
        }

        return sentInts;

    }

    private Integer CharToInt(String character) {
        Preconditions.checkNotNull(character);
        Integer value = vocabularyIndexMap.get(character);
        if (value == null) {
            return unkIndex;
        } else {
            return value;
        }
    }

    public static boolean Repeat(List<String> sent, float ratio) {
        Set<String> set = new HashSet<String>();
        Integer sum = sent.size();
        List<String> uniqKey = new ArrayList<>();
        for (String word : sent) {
            if (!uniqKey.contains(word)) {
                uniqKey.add(word);
            }

        }
        Integer uniq_sum = uniqKey.size();
        float result = (float) uniq_sum / sum;
        return result < ratio;


    }

    public static List<List<String>> Evaluator(List<List<String>> totalString, float ratio) {
        List<List<String>> newStrings = new LinkedList<List<String>>();
        for (List<String> sent : totalString) {
            if (sent.size() >= 4 && !DataPreprocessorImpl.Repeat(sent, ratio)) {
                newStrings.add(sent);
            }

        }
        if (newStrings.size() == 0) {

            newStrings.add(totalString.get(0));


        }
        return newStrings;
    }


    public List<String> IntstoSentence(List<Integer> ints) {
        Preconditions.checkNotNull(ints);
        List<String> sentence = Lists.newArrayList();
        for (int num : ints) {
            sentence.add(IntoChar(num));
        }
        return sentence;
    }

    private String IntoChar(Integer num) {
        Preconditions.checkNotNull(num);

        String word = IndexVocaMap.get(num);
        if (word != null) {
            return word;
        } else {
            return IndexVocaMap.get(unkIndex);
        }
    }

}
