import os 
import sys
import json

from dotenv import load_dotenv

load_dotenv()

MONGODB_URL=os.getenv("MONGODB_URL")
print(MONGODB_URL)

# communicate with mongodb we have certified buddle of certificate stpre in certifiate authority
import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo 
from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging

class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
            
        except Exception as e:
            raise NetWorkSecurityException(e,sys)
            pass
    
    def csv_to_json_conveter(self,file_path):
        try:
            data=pd.read_csv(file_path)
           # drop_index=data.drop([index])
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetWorkSecurityException(e,sys)    
        
    def  insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGODB_URL) 
            
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))

        except Exception as e:
            raise NetWorkSecurityException(e,sys)
        

if __name__ == "__main__":
    FILE_PATH="data\Phising_website_data.csv"        
    DATABASE="LATHAAI"
    collection="networkData"
    network_obj=NetworkDataExtraction()
    records=network_obj.csv_to_json_conveter(file_path=FILE_PATH)
    print(records)
    no_of_records=network_obj.insert_data_mongodb(records,DATABASE,collection)
    print(no_of_records)
          