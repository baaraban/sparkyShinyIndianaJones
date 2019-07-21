import re

from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from pyspark.sql.functions import pandas_udf, PandasUDFType
from preprocessing.preprocessors.abstraction.BasePreprocessor import BasePreprocessor
from utils.text_parser import TextParser
from datetime import datetime
import pandas as pd


class WikiPreprocessor(BasePreprocessor):
    _parser = None

    @staticmethod
    def get_parser():
        if not WikiPreprocessor._parser:
            WikiPreprocessor._parser = TextParser()
        return WikiPreprocessor._parser

    def get_data_source_name(self):
        return "Wiki data"

    def get_matching_regex(self):
        return re.compile(r'.*wikidata.*\.csv')

    def preprocess(self, dataframe):
        current_date = str(datetime.now())
        new_df = dataframe.withColumn("movement_dates", get_movement_dates("text", "title"))
        new_df = new_df.withColumn("creation_date",
                                when(col('inception').isNull() | col('country').isNull(), "{}")\
                                .otherwise("{" + col('inception') + ":" + col('country') + "}"))
        new_df = new_df.withColumn("acquiring_date",
                                   when(col('location').isNull(), "{}") \
                                   .otherwise("{" + current_date + ":" + col('location') + "}"))
        new_df = new_df.withColumnRenamed("image", "image_link")
        new_df = new_df.withColumnRenamed("title", "artifact_name")
        new_df = new_df.withColumn("transitions", concat('acquiring_date', 'creation_date', 'movement_dates'))
        return new_df[['artifact_name', 'transitions', 'image_link']]


@pandas_udf(returnType=StringType(), functionType=PandasUDFType.SCALAR)
def get_movement_dates(documents, titles):
    parser = WikiPreprocessor.get_parser()

    def prepare_element(x):
        if not x:
            return None
        return x.split('Bibliography')[0].strip().replace('\n', '. ').replace('\t', '')

    def get_title(title):
        return str(title)[0].strip('(')

    def get_element(x, aliases):
        if not x:
            return '{}'
        transitions = parser.parse_entity_movement(x, aliases)
        if transitions:
            return str(transitions)
        else:
            return '{}'

    return pd.Series([get_element(prepare_element(x[0]), [get_title(x[1])]) for x in zip(documents, titles)])
