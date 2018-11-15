package com.jd.jnlu.nlg.model;

import java.util.List;

public class DataEntry {
    public final int[] source;
    public final int[] sourceLen;
    //public final List<String> sentence;

    public DataEntry(int[] source, int []sourceLen) {
        this.source = source;
        this.sourceLen = sourceLen;
        //this.sentence=sentence;

    }
}
