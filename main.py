from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging
from src.networksecurity.entity.config_entity import DataIngestionConfig
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
        print(dataingestionartifact)
    except Exception as e:
        raise NetWorkSecurityException(e,sys) 