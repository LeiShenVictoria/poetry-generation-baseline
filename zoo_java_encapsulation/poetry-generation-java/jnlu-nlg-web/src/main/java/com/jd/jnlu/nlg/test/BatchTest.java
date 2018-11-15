package com.jd.jnlu.nlg.test;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.List;

public class BatchTest {

	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		
		String path1 = "./jnlu-nlg-web/src/resources/test/test_fushi_50_0706.key";
		String path2 = "./jnlu-nlg-web/src/resources/test/test_fushi_50_0706.out";
		String vocabPath = "./jnlu-nlg-web/src/resources/dict/vocab_fushi.txt";
		String modelPath = "./jnlu-nlg-web/src/resources/model/minimal_graph_fushi.proto";
		NLGModelTest instance = new NLGModelTest(vocabPath, modelPath);
		
		BufferedReader br1 = new BufferedReader(new InputStreamReader(new FileInputStream(new File(path1))));
		BufferedWriter bw1 = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(path2))));
		String line = null;
		while((line = br1.readLine()) != null) {
			String[] arr = line.split("\t");
			if(arr.length < 2) {
				continue;
			}
			String label = arr[0];
			String keywords_str = arr[1];
			List<String> sentences = instance.process(keywords_str);
			System.out.println(sentences);

			bw1.write(label+"\r\n");
			bw1.write("Keywords:"+keywords_str+"\r\n");
			for(String str : sentences) {
				bw1.write(str+"\r\n");
			}
			bw1.write("\r\n");
			
		}
		br1.close();
		bw1.close();
		
		
	}

}
