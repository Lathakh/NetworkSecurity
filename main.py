from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.components.data_validation import DataValidation
from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging
from src.networksecurity.entity.config_entity import DataIngestionConfig
from src.networksecurity.entity.config_entity import DataValidationConfig
from src.networksecurity.entity.config_entity import TrainingPipelineConfig
import os
import sys


if __name__ == '__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()

        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)

        logging.info("initate the data ingestion")

        dataingestionartifact=data_ingestion.initiate_data_ingestion()

        logging.info("data initiated completed")
        print(dataingestionartifact)

        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)

        logging.info("initate the data valdation")

        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifact)
    except Exception as e:
        raise NetWorkSecurityException(e,sys) 