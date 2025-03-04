import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline 

from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging

from src.networksecurity.constant.training_pipeline import TARGET_COLUMN
from src.networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from src.networksecurity.entity.artifact_entity import (DataTransformationArtifact , DataValidationArtifact)
from src.networksecurity.entity.config_entity import DataTransformationConfig
from src.networksecurity.utils.common import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact= data_validation_artifact
            self.data_transformation_config:DataTransformationConfig= data_transformation_config

        except Exception as e:
            raise NetWorkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
           return pd.read_csv(file_path)

        except Exception as e:
            raise NetWorkSecurityException(e,sys)

    def get_transformation_object(cls)->Pipeline:
        """ it initiatialize a KNN iMputer object with parameters specified in in traiing_pipeline.py file
        and return pipeline object with the KNNImputer object as first step
        arg:
        cls- DataTransformation 

        Returns:
        Apipeline object
        """
        logging.info("enter the get_data_transformation in Datatransformation class")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) # what ever paramneter you give it consider as key value pair
            logging.info("intialize the KNNIMputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        
        except Exception as e:
            raise NetWorkSecurityException(e,sys)


        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("enter the initiate data transformation")

        try:
            # we need to read the trai and test data
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            #training datframe
            input_feature_train_df=train_df.drop(columns=["index","Result"],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df= target_feature_train_df.replace(-1,0)
            
            # testing data frame
            input_feature_test_df=test_df.drop(columns=["index","Result"],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df= target_feature_test_df.replace(-1,0)

            #
            preprocessor_object=self.get_transformation_object()

            preprocessor_object=preprocessor_object.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            #save the nupy array to craete pickle file
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)

            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)

            #preprating artifact

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise NetWorkSecurityException(e,sys)
