import logging
import os 
from datetime import datetime

# log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# defining log file path
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s ] %(lineno)d %(name)s-%(levelname)s - %(message)s",
    level=logging.INFO
)
