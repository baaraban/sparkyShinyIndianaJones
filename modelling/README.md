# Modelling

The main purpose of modelling was to build the system which extracts movements of entity from text description of it. <br>
This was unsupervised learning task as we didn't have labelled data. We encorporated different open-source pre-trained model to achieve our goal. <br>
This part of the project contains jupyter notebooks with our researches and intermediate results. <br>
Final model can be found in utils/text_parser.py file

## Named entity recognitions

We started our developing with Named Entity Recognition problem. <br>
We tried and compared three pre-trained models available for Spacy package (en_core_web_sm, en_core_web_md, en_core_web_lg), 
model from deeppavlov package and model from polyglot package. <br>
The results which these models demonstrated can be found in accordingly named .ipynb files.

## Word disambiguation task
We tried to develop the system which can track and detect mentioning of concrete artifact throughout a text. <br>
The main idea was to replace all mentioning of entity with some token('ENTITY' etc.) which can be easily detected afterwards. <br>
For this task we used combination of language model provided by spacy and package textacy. <br>
The results were not sufficient enough to use it in our TextParser class
