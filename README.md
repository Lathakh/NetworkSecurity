# Network security project for phising data

## 1.created new repo in github.com

## 2.project structure folder created
## 3.installed new environment(network) and install the requirement .txt  and setup.py
## 4.written code for logging and exception handling.
## 5.logint to mongoDB atlas and connect with DB   --- test_mongodb.py
## 5.ETL Pipleine code to convert i to json format and push into mangodb atlas  -- push_data.py

## 6. DataINgestion Component
    1.components
        ----> CREATE --- data_ingetion.py
    2.constant
        -----> CREATE-- training_pipeline.py
                        create --- __init__.py 
        
    3.entity
        ----->CREATE --- Config_entity.py  
        ----->CREATE--- Artifact_entity.py
        
    OUT PUT OF DATAINGESTION IS Artifact folder
                                --CREATED--- feature_store folder
                                                -- Raw_data: Phising_website_data.csv
                                --CREATED--- Ingested folder
                                                -- Split data: Train.csv, test.csv files                



##
