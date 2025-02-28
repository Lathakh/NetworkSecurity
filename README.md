# Network security project for phising data

### 1.created new repo in github.com

### 2.project structure folder created
### 3.installed new environment(network) and install the requirement .txt  and setup.py
### 4.written code for logging and exception handling.
### 5.logint to mongoDB atlas and connect with DB   --- test_mongodb.py
### 5.ETL Pipleine code to convert i to json format and push into mangodb atlas  -- push_data.py

### 6. DataINgestion Component
    1.components
        ----> CREATE --- data_ingetion.py
                           Class: DataIngestion
                           functions: 0. __init__ constructor 
                                     1. export_collection_as_dataframe
                                     2. split_data_as_train_test
                                     3. initiate_data_ingestion
                           

    2.constant
        -----> CREATE-- training_pipeline.py
                        create --- __init__.py 
                                    1.defining common constant variable for training pipeline
                                    2.DATA Ingestion related constant start with DATAINGESTION VAR NAME

        
    3.entity
        ----->CREATE --- Config_entity.py 
                            Class : 1.TrainingPipelineConfig
                            function:__init__ constructure

                            Class : 2.DataIngestionConfig
                            functions: 1. __init__ defined path of all oupr of dta ingestion
                            
        ----->CREATE--- Artifact_entity.py
                            class DataIngestionArtifact:
                                    trained_file_path:str
                                     test_file_path:str
        
    OUT PUT OF DATAINGESTION IS Artifact folder
                                --CREATED--- feature_store folder
                                                -- Raw_data: Phising_website_data.csv
                                --CREATED--- Ingested folder
                                                -- Split data: Train.csv
                                                               test.csv file              



###
