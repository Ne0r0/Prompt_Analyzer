import logging
import os 

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

logger = logging.getLogger("text_analyzer")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f"{log_folder}/app.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)

logging.getLogger("wekzeug").setLevel(logging.WARNING)