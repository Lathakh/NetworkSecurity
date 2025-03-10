from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.components.data_validation import DataValidation
from src.networksecurity.components.data_transformation import DataTransformation
from src.networksecurity.components.model_trainer import ModelTrainer
from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging
from src.networksecurity.entity.config_entity import (TrainingPipelineConfig,DataIngestionConfig,
                                                      DataValidationConfig,DataTransformationConfig,ModelTrainerConfig)

import os
import sys

if __name__ == '__main__':
    try:
        # #  DATA INGESTION STEP PIPELINE
        logging.info("--------Data Ingestion Started--------")
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("initated the class data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("---------data Ingestion completed-------")

##  DATA VALIDATION STEP PIPELINE       
        logging.info("--------Data Validation Started--------")
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info("initate the data valdation")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("--------data validation completed-------")
        
#  DATA TRANSFORMATION STEP PIPELINE

        logging.info("-------started the data transformation-------")
        datatransformationconfig=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact, datatransformationconfig)
        logging.info("initated the data transformation class ")
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("--------completed the data transformation-------")
        
#  Model trainer and evaluationmSTEP PIPELINE
        logging.info("-------started the data modeling-------")
        model_trainer_conf=ModelTrainerConfig(trainingpipelineconfig)
        data_trainer=ModelTrainer(model_trainer_conf=model_trainer_conf,data_transformation_artifact=data_transformation_artifact)
        logging.info("Model training and evaluatin  initated method ")
        model_trainer_artifact=data_trainer.initiate_model_trainer()

        print(model_trainer_artifact)
        logging.info("--------completed the model and evalaution-------")
        


    except Exception as e:
        raise NetWorkSecurityException(e,sys) 