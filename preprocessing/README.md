# Preprocessing
## Overview
This folder contains main preprocessing part which is using pySpark.
main.ipynb file does all the work. <br>
It uses supportive code which can be found in 'preprocessors' folder.
## Architecture and general approach description
ProcessingWorker - is the class which is the entry point to preprocessing job. <br>
During the creation it receives sparkSession and list of implementations of BasePreprocessor class. <br>
Because we are using different data sources the preprocessing can't be unified. <br>
Right now, we have to preprocessors: LouvrePreprocesser and WikiPreprocessor. Each of them knows the regex which allows to find needed file for dataframe,
and has defined 'preprocess' function which transforms the dataframe to unified structure.<br>
Transformed dataframes are saved by ProcessingWorker to /prepared_data/partitioned folder.

## Explanation on why we used pandas_udf
We encountered some difficulties with running Spacy model in classical udf. <br>
There was a serialization problem for Spacy model, so we added lazy loading of TextParser class. <br>
After this there was some mismatch with the way Java Runtime and python treat OS paths(spacy couldn't load en_core_web model)<br>
Switching to pandas_udf made the difference 
