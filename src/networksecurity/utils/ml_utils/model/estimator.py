# model info

from src.networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
import sys


from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:

            self.preprocessor = preprocessor
            self.model=model
        except Exception as e:
            raise NetWorkSecurityException(e,sys)    
        

    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)  # transform ationf or new data 
            y_hat=self.model.predict(x_transform)  # predict for new data
            return y_hat
        except Exception as e:
            raise NetWorkSecurityException(e,sys)    

