from abc import ABC, abstractmethod


class BasePreprocessor(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_data_source_name(self):
        pass

    @abstractmethod
    def get_matching_regex(self):
        pass

    @abstractmethod
    def preprocess(self, dataframe):
        pass
