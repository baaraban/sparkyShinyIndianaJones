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
        new_df = dataframe.withColumn("acquiring_dates", get_acquiring_dates(dataframe["acquired_by"]))
        new_df = new_df.withColumn("image_link", transform_image_link("image_link"))
        return new_df


@pandas_udf(returnType=StringType(), functionType=PandasUDFType.SCALAR)
def get_acquiring_dates(documents):
    parser = LouvrePreprocessor.get_parser()

    def get_element(x):
        dates = parser.get_dates(str(x))
        if len(dates) == 0:
            return ""
        else:
            return str({dates[0] : LouvrePreprocessor.get_louvre_location()})

    return pd.Series([get_element(x) for x in documents])


@udf(returnType = StringType())
def transform_image_link(img_link):
    literal = 'https://www.louvre.fr'
    return str(img_link)[len(literal):]
