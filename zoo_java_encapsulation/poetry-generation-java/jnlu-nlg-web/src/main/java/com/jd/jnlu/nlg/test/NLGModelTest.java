package com.jd.jnlu.nlg.test;

import com.google.common.collect.Lists;
import com.jd.jnlu.nlg.model.*;
import org.apache.avro.generic.GenericData;
import org.junit.Test;

import java.io.IOException;
import java.lang.reflect.Array;
import java.util.*;
import org.tensorflow.*;

public class NLGModelTest {

    public String vocabPath ;
    public String modelPath ;

    public NLGModelTest(){

    }
    public NLGModelTest(String vocabPath, String modelPath){
        this.vocabPath = vocabPath;
        this.modelPath = modelPath;
    }

    public static void main (String args[]){
        String vocabPath = "./jnlu-nlg-web/src/resources/dict/vocab_fushi.txt";
        String modelPath = "./jnlu-nlg-web/src/resources/model/minimal_graph_fushi.proto";

        long start_time = System.currentTimeMillis();

        String keywords_str = "文艺,优雅 简约 修身,连衣裙"; //  文艺,优雅 简约 修身,连衣裙    裸色 专业 潮流   化妆水 面霜,紧致 精华,液体   文艺,轻奢 卧室,衣帽架 专业,实用

        NLGModelTest instance = new NLGModelTest(vocabPath, modelPath);
        try {
            List<String> sentences = instance.process(keywords_str);
            for(String str : sentences){
                System.out.println(str);
            }
        }catch (Exception e){
            e.printStackTrace();
        }

        long end_time = System.currentTimeMillis();

        System.out.println("use time: " + (end_time-start_time));



    }


    public List<String> process(String keywords_str) throws IOException {

//        String vocabPath = "./jnlu-nlg-web/src/resources/dict/vocab_fushi.txt";
//        String modelPath = "./jnlu-nlg-web/src/resources/model/minimal_graph_fushi.proto";
        DataPreprocessorImpl dataPreprocessor = new DataPreprocessorImpl(vocabPath);
        NLGTensorflowModel nlgTensorflowModel = new NLGTensorflowModel(modelPath);

        List<String> sentences = new ArrayList<String>();
        boolean reverse = true;
        boolean Re_rank=true;
        float ratio = 0.34f;
        int stop_num = 10599;
        int prev_num = 4;

        String[] arr = keywords_str.split(" ");

        List<List<String>> previous = new LinkedList<List<String>>();

        for(int m = 0;m < arr.length;m++){

            String keystr = arr[m];
            String[] key_arr = keystr.split(",");

            List<List<String>> keywords = new ArrayList<List<String>>();
            for(int n = 0;n < key_arr.length;n++){
                char[] chas = key_arr[n].toCharArray();
                List<String> keyword1 = new ArrayList<>();
                for(char c : chas){
                    keyword1.add(String.valueOf(c));
                }
                keywords.add(keyword1);
            }

            DataEntry dataEntry = dataPreprocessor.preprocess(keywords, previous, reverse);
            int[][] output = nlgTensorflowModel.predict(dataEntry);
            //long num_len=tensor.shape()[2];
            long beam_with = output[0].length;
            //int index=(int)(Math.random()*beam_with)Y;

            List<List<Integer>> new_out = new LinkedList<List<Integer>>();

            int length = output.length;
            int width = (int) beam_with;


            for (int j = 0; j < width; j++) {
                List<Integer> int_list = new ArrayList<>();
                for (int i = 0; i < length; i++) {
                    int ele = output[i][j];
                    if (ele != stop_num) {
                        int_list.add(ele);
                    } else {
                        break;
                    }
                }
                new_out.add(int_list);
            }

            List<List<String>> total_string = new LinkedList<List<String>>();
            for (List<Integer> ele : new_out) {
                if (reverse) {
                    Collections.reverse(ele);
                }
                List<String> outputStringList = dataPreprocessor.IntstoSentence(ele);
                total_string.add(outputStringList);

            }
            List<List<String>> newStrings = new LinkedList<List<String>>();
            if (Re_rank) {
                List<List<String>> newStrings1= DataPreprocessorImpl.Evaluator(total_string,ratio);
                newStrings= newStrings1;

            }else{
                newStrings = total_string;
            }

            int index = (int)(Math.random()*newStrings.size());

            List<String> random_sent = newStrings.get(index);

            StringBuffer buffer = new StringBuffer();
            for(String str : random_sent){
                buffer.append(str);
            }
            if(m == arr.length-1){
                buffer.append("。");
            }else{
                buffer.append("，");
            }
            sentences.add(buffer.toString());

            if(previous.size() < prev_num){
                previous.add(random_sent);
            }else{
                previous.remove(0);
                previous.add(random_sent);
            }


        }

        return sentences;

    }

}
