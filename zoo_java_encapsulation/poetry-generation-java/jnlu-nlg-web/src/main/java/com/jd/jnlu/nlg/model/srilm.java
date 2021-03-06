package com.jd.jnlu.nlg.model;/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 2.0.10
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */


import com.jd.jnlu.nlg.model.srilmJNI;

public class srilm {
  public static SWIGTYPE_p_Ngram initLM(int order) {
    long cPtr = srilmJNI.initLM(order);
    return (cPtr == 0) ? null : new SWIGTYPE_p_Ngram(cPtr, false);
  }

  public static void deleteLM(SWIGTYPE_p_Ngram ngram) {
    srilmJNI.deleteLM(SWIGTYPE_p_Ngram.getCPtr(ngram));
  }

  public static long getIndexForWord(String s) {
    return srilmJNI.getIndexForWord(s);
  }

  public static String getWordForIndex(long i) {
    return srilmJNI.getWordForIndex(i);
  }

  public static int readLM(SWIGTYPE_p_Ngram ngram, String filename) {
    return srilmJNI.readLM(SWIGTYPE_p_Ngram.getCPtr(ngram), filename);
  }

  public static float getWordProb(SWIGTYPE_p_Ngram ngram, long word, SWIGTYPE_p_unsigned_int context) {
    return srilmJNI.getWordProb(SWIGTYPE_p_Ngram.getCPtr(ngram), word, SWIGTYPE_p_unsigned_int.getCPtr(context));
  }

  public static float getNgramProb(SWIGTYPE_p_Ngram ngram, String ngramstr, long order) {
    return srilmJNI.getNgramProb(SWIGTYPE_p_Ngram.getCPtr(ngram), ngramstr, order);
  }

  public static float getUnigramProb(SWIGTYPE_p_Ngram ngram, String word) {
    return srilmJNI.getUnigramProb(SWIGTYPE_p_Ngram.getCPtr(ngram), word);
  }

  public static float getBigramProb(SWIGTYPE_p_Ngram ngram, String ngramstr) {
    return srilmJNI.getBigramProb(SWIGTYPE_p_Ngram.getCPtr(ngram), ngramstr);
  }

  public static float getTrigramProb(SWIGTYPE_p_Ngram ngram, String ngramstr) {
    return srilmJNI.getTrigramProb(SWIGTYPE_p_Ngram.getCPtr(ngram), ngramstr);
  }

  public static float getSentenceProb(SWIGTYPE_p_Ngram ngram, String sentence, long length) {
    return srilmJNI.getSentenceProb(SWIGTYPE_p_Ngram.getCPtr(ngram), sentence, length);
  }

  public static float getSentencePpl(SWIGTYPE_p_Ngram ngram, String sentence, long length) {
    return srilmJNI.getSentencePpl(SWIGTYPE_p_Ngram.getCPtr(ngram), sentence, length);
  }

  public static int numOOVs(SWIGTYPE_p_Ngram ngram, String sentence, long length) {
    return srilmJNI.numOOVs(SWIGTYPE_p_Ngram.getCPtr(ngram), sentence, length);
  }

  public static long corpusStats(SWIGTYPE_p_Ngram ngram, String filename, SWIGTYPE_p_TextStats stats) {
    return srilmJNI.corpusStats(SWIGTYPE_p_Ngram.getCPtr(ngram), filename, SWIGTYPE_p_TextStats.getCPtr(stats));
  }

  public static float getCorpusProb(SWIGTYPE_p_Ngram ngram, String filename) {
    return srilmJNI.getCorpusProb(SWIGTYPE_p_Ngram.getCPtr(ngram), filename);
  }

  public static float getCorpusPpl(SWIGTYPE_p_Ngram ngram, String filename) {
    return srilmJNI.getCorpusPpl(SWIGTYPE_p_Ngram.getCPtr(ngram), filename);
  }

  public static int howManyNgrams(SWIGTYPE_p_Ngram ngram, long order) {
    return srilmJNI.howManyNgrams(SWIGTYPE_p_Ngram.getCPtr(ngram), order);
  }

}
