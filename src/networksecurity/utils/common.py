import yaml
from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging
from src.networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn.model_selection import GridSearchCV
import os
import sys
import numpy as np
#import dill
import pickle


def read_yaml_file(file_path:str)-> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetWorkSecurityException(e,sys)
    


def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
                    
    except Exception as e:
        raise  NetWorkSecurityException(e,sys)
    
def save_numpy_array_data(file_path: str ,array:np.array):
    """"Save the numpy array data file
    file_path: str location of file to save
    array: np.array data to save
    """    

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise NetWorkSecurityException(e,sys)
    
# modeltrainer
def save_object(file_path: str, obj:object):
    try:
        logging.info("entered the save_object method of utils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save object  functio in  utils folder")    
    except Exception as e:
        raise NetWorkSecurityException(e,sys)

def load_object(file_path: str, )->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"file path {file_path} does not exist")
     
        with open(file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
        
    except Exception as e:
        raise NetWorkSecurityException(e,sys) from e

def load_numpy_array_data(file_path: str)-> np.array:
    """"load the numpy array data file
    file_path: str location of file to load
    array: np.array data to load
    """    

    try:
       
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise NetWorkSecurityException(e,sys) from e
    



def evaluate_model(X_train, X_test,y_train,y_test,models,param):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs=GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            #model.fit(X_train,y_train)

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_model_score=recall_score(y_train,y_train_pred)
            test_model_score=recall_score(y_test,y_test_pred)

            report[list(models.keys())[i]]=test_model_score

        return report    



    except Exception as e:
        raise NetWorkSecurityException(e,sys)
    
