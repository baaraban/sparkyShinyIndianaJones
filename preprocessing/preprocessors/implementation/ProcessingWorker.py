from utils import os_utils
from tqdm import tqdm


class ProcessingWorker:
    def __init__(self, preprocessors, saving_path, spark_session):
        self.preprocessors = preprocessors
        self.saving_path = saving_path
        self.session = spark_session
        super().__init__()

    def _execute_preprocessor(self, prep):
        files_to_process = os_utils.get_files_rec(prep.get_matching_regex())
        for file in files_to_process:
            df = self.session.read.csv(path=file, sep=',',
                                  inferSchema=False, charToEscapeQuoteEscaping='"',
                                  header='true', escape='"', multiLine=True)

            df = prep.preprocess(df)

            path = f'{self.saving_path}/{prep.get_data_source_name()}.csv'
            #df.repartition(1).write.format('com.databricks.spark.csv').save(path, header='true')
            df.toPandas().to_csv(f'{self.saving_path}/{prep.get_data_source_name()}.csv', index=False)

    def execute_preprocessors(self):
        for prep in tqdm(self.preprocessors):
            self._execute_preprocessor(prep)
