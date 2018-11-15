package com.jd.jnlu.nlg.model;

import java.util.List;

public interface DataPreprocessor {
    DataEntry preprocess(List<String> keyword, List<List<String>> previous,Boolean reverse);
}
