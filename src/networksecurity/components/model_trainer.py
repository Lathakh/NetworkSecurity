import os
import sys

from src.networksecurity.exception.exception import NetWorkSecurityException
from src.networksecurity.logging.logger import logging

from src.networksecurity.entity.artifact_entity import (DataTransformationArtifact ,ModelTrainerArtifact)
from src.networksecurity.entity.config_entity import ModelTrainerConfig

from src.networksecurity.utils.common import save_numpy_array_data,save_object
from src.networksecurity.utils.common import load_numpy_array_data,load_object
from src.networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from src.networksecurity.utils.ml_utils.model.estimator import NetworkModel
from src.networksecurity.utils.common import evaluate_model


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow


class ModelTrainer:
    def __init__(self,model_trainer_conf:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_conf=model_trainer_conf
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetWorkSecurityException(e,sys)
        

    def track_mlflow(self,best_model,classificationmatric):
         with mlflow.start_run():
              f1_score=classificationmatric.f1_score
              precision_score=classificationmatric.precision_score
              recall_score=classificationmatric.recall_score

              mlflow.log_metric("f1_score",f1_score)
              mlflow.log_metric("precision_score",precision_score)
              mlflow.log_metric("recall_score",recall_score) 
              mlflow.sklearn.log_model(best_model,"model")   
                
    def train_model(self,X_train,y_train,X_test,y_test):
            
            models={
                 "Random Forest": RandomForestClassifier(verbose=1),
                 "Decision Tree": DecisionTreeClassifier(),
                 "Gradient Boosting classifier":GradientBoostingClassifier(verbose=1),
                 "Logistic Regression": LogisticRegression(verbose=1),
                 "Ada Boosting classifier":AdaBoostClassifier(),
                                                         
                 }
                                                    
            # Hyperparameter tuning
            params={
                 "Decision Tree":{
                      'criterion':["gini","entropy","log_loss"],
                      #'splitter':['best','random'],
                      #'max_features':['sqrt','log2']
                 },
                 "Random Forest":{
                      #'criterion':["gini","entropy","log_loss"],
                      
                      #'max_features':['sqrt','log2',None]
                      'n_estimators':[8,16,32]
                 },
                 "Gradient Boosting classifier":{
                      #'loss':["log_loss","exponential"],
                      'learning_rate':[0.1,0.01,0.001],
                      'subsample':[0.6,0.7,],

                      #'criterion':["squared_error","friedman_mse"],
                      #'max_features':['auto','sqrt','log2],
                      'n_estimators':[8,16,32]
                 },
                 "Logistic Regression":{},
                 "Ada Boosting classifier":{
                      'learning_rate':[0.1,0.001],
                      'n_estimators':[8,16]
                 }
            }
            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)
            ##to get the best model
            best_model_score=max(sorted(model_report.values()))
            # best model name from dictionary
            best_model_name=list(model_report.keys())[
                 list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]


            y_train_pred=best_model.predict(X_train)
            classification_train_matric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
            

            ## to track  experiement with Ml flow
            self.track_mlflow(best_model,classification_train_matric)

            y_test_pred=best_model.predict(X_test)
            classification_test_matric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
            self.track_mlflow(best_model,classification_test_matric)

            preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path=os.path.dirname(self.model_trainer_conf.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_conf.trained_model_file_path,obj=network_model)

            # model pusher to any cloud here i am pusing to local folder 
            save_object("final_model/model.pkl",best_model)    

            #model trainer artifact

            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_conf.trained_model_file_path,
                                 train_metric_artifact=classification_train_matric,
                                 test_metric_artifact=classification_test_matric)
            

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            #load data from train file path  and test array
            train_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],  # lost column
                test_arr[:,:-1],
                test_arr[:,-1]  # lost column
            )
            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)

            return model_trainer_artifact


        except Exception as e:
            raise NetWorkSecurityException(e,sys)    