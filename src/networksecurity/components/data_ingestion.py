from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging


## configuration of data inegstion config

from src.networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from src.networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv("MONGODB_URL")
print(MONGODB_URL)
logging.info("successfully connected to mongoDB!")



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetWorkSecurityException(e,sys)
        
    # read the dataframe from mongoDB and written Dataframe
    def export_collection_as_dataframe(self):
        try :
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

        # Ensure MongoDB client is using correct URL
            self.mongo_client = pymongo.MongoClient(MONGODB_URL)

            collection = self.mongo_client[database_name][collection_name]

        # Fetch data, excluding '_id' field directly in query
            df = pd.DataFrame(list(collection.find({}, {'_id': 0})))  

        # Handle missing values
            df.replace({"na": np.nan}, inplace=True)

            return df
            """database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGODB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            ## by default _id columns will be added while read data
            if "_id"in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df"""

        except Exception as e:
            raise NetWorkSecurityException(e,sys)    

# extract the data from mongdb to feature store

    def extract_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_path
            #craete folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
                    
        except Exception as e:
            raise NetWorkSecurityException(e,sys)


    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("performed train test split on the dataframe")
            logging.info("exited split_data_as_train_test method of DataIngestion Class")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("exporting  train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info("exported train and test file path")

        except Exception as e:
            raise NetWorkSecurityException(e,sys)



    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.extract_data_into_feature_store(dataframe) 
            self.split_data_as_train_test(dataframe)
            dataIngestionArtifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataIngestionArtifact


        except Exception as e:
            raise NetWorkSecurityException(e,sys)

# read from mongoDB
