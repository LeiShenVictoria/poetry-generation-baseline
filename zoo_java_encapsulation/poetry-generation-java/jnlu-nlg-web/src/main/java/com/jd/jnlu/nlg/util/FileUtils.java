package com.jd.jnlu.nlg.util;

import com.beust.jcommander.internal.Maps;
import com.google.common.base.Preconditions;
import com.google.common.io.Closeables;
import edu.stanford.nlp.io.IOUtils;
import org.assertj.core.util.Lists;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.List;
import java.util.Map;

/**
 * Created by chenyong6 on 2018/2/1
 */
public class FileUtils {
    public static Map<String, String> loadData(String path) throws IOException{
        Preconditions.checkNotNull(path);
        Map<String, String> rst = Maps.newHashMap();
        BufferedReader bufferedReader = IOUtils.readerFromString(path);
        try {
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                String[] strs = line.split("\t");
                if (strs.length != 2){
                    continue;
                }
                String words = strs[0];
                String intent = strs[1];
                rst.put(words, intent);
            }
        } finally {
            Closeables.closeQuietly(bufferedReader);
        }
        return rst;
    }

    public static List<String> loadDataToList(String path) throws IOException{
        Preconditions.checkNotNull(path);
        List<String> rst = Lists.newArrayList();
        BufferedReader bufferedReader = IOUtils.readerFromString(path);
        try {
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                if (line.length() < 1){
                    continue;
                }
                rst.add(line);
            }
        } finally {
            Closeables.closeQuietly(bufferedReader);
        }
        return rst;
    }

}
