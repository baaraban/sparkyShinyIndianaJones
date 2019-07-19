import re

from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from pyspark.sql.functions import pandas_udf, PandasUDFType
from preprocessing.preprocessors.abstraction.BasePreprocessor import BasePreprocessor
from utils.text_parser import TextParser
from utils.location_utils import get_lat_lon
import pandas as pd


class LouvrePreprocessor(BasePreprocessor):
    _louvre_location = get_lat_lon("Louvre")
    _parser = None

    @staticmethod
    def get_parser():
        if not LouvrePreprocessor._parser:
            LouvrePreprocessor._parser = TextParser()
        return LouvrePreprocessor._parser

    @staticmethod
    def get_louvre_location():
        return LouvrePreprocessor._louvre_location

    def get_data_source_name(self):
        return "Louvre official site data"

    def get_matching_regex(self):
        return re.compile(r'.*louvre.*\.csv')

    def preprocess(self, dataframe):
        new_df = dataframe.withColumn("movement_dates", get_movement_dates("text"))
        new_df = new_df.withColumn("acquiring_date", get_acquiring_dates("acquired_by"))
        new_df = new_df.withColumn("creation_date", get_creation_dates("creation_info"))
        new_df = new_df.withColumn("image_link", transform_image_link("image_link"))
        new_df = new_df.withColumn("transitions", concat('acquiring_date', 'creation_date', 'movement_dates'))
        return new_df[['artifact_name', 'transitions', 'image_link']]


@pandas_udf(returnType=StringType(), functionType=PandasUDFType.SCALAR)
def get_movement_dates(documents):
    parser = LouvrePreprocessor.get_parser()

    def prepare_element(x):
        return x.split('Bibliography')[0].strip().replace('\n', '. ').replace('\t', '')

    def get_element(x):
        transitions = parser.get_text_date_location_per_sentence(x)
        if transitions:
            return str(transitions)
        else:
            return ''

    return pd.Series([get_element(prepare_element(x)) for x in documents])


@pandas_udf(returnType=StringType(), functionType=PandasUDFType.SCALAR)
def get_creation_dates(documents):
    parser = LouvrePreprocessor.get_parser()

    def get_element(x):
        transition = parser.get_single_date_location_pair(x)
        if transition:
            return str(transition)
        else:
            return '{}'

    return pd.Series([get_element(x) for x in documents])


@pandas_udf(returnType=StringType(), functionType=PandasUDFType.SCALAR)
def get_acquiring_dates(documents):
    parser = LouvrePreprocessor.get_parser()

    def get_element(x):
        dates = parser.get_dates(str(x))
        if len(dates) == 0:
            return '{}'
        else:
            return str({dates[0] : LouvrePreprocessor.get_louvre_location()})

    return pd.Series([get_element(x) for x in documents])


@pandas_udf(returnType=StringType(), functionType=PandasUDFType.SCALAR)
def transform_image_link(img_links):
    literal = 'https://www.louvre.fr'
    return img_links.apply(lambda x: str(x)[len(literal):])
