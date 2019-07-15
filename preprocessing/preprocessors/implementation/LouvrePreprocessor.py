import re

from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from preprocessing.preprocessors.abstraction.BasePreprocessor import BasePreprocessor


class LouvrePreprocessor(BasePreprocessor):
    def get_data_source_name(self):
        return "Louvre official site data"

    def get_matching_regex(self):
        return re.compile(r'.*louvre.*\.csv')

    def get_transformation_dict(self):
        return {
            ("image_link", "image_link"): udf(lambda z: LouvrePreprocessor.transform_image_link(z), StringType())
        }

    # Transform functions
    @staticmethod
    def transform_image_link(img_link):
        literal = 'https://www.louvre.fr'
        return str(img_link)[len(literal):]
