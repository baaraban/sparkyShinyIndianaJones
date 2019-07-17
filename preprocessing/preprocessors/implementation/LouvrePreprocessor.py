import re

from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from preprocessing.preprocessors.abstraction.BasePreprocessor import BasePreprocessor
from utils.text_parser import TextParser
from utils.location_utils import get_lat_lon


class LouvrePreprocessor(BasePreprocessor):
    def __init__(self):
        self._parser = TextParser()
        self._louvre_location = get_lat_lon("Louvre")

    def get_data_source_name(self):
        return "Louvre official site data"

    def get_matching_regex(self):
        return re.compile(r'.*louvre.*\.csv')

    def get_transformation_dict(self):
        return {
            ("image_link", "image_link"): udf(lambda z: LouvrePreprocessor.transform_image_link(z), StringType()),
            ("acquired_by", "louvre_related"): udf(lambda z: LouvrePreprocessor.get_louvre_transition(z), StringType())
        }

    # Transform functions
    @staticmethod
    def transform_image_link(img_link):
        literal = 'https://www.louvre.fr'
        return str(img_link)[len(literal):]

    def get_louvre_transition(self, text):
        dates = self._parser.get_dates(text.strip())
        if len(dates) == 0:
            return ""
        else:
            return f"{dates[0]} : {self._louvre_location}"
