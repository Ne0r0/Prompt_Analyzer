import logging
import coloredlogs
import os 

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

# Creating a shared logger
logger = logging.getLogger("text_analyzer")
logger.setLevel(logging.INFO)

# Coloured logs for terminal
coloredlogs.install(
    level=logging.INFO,
    logger=logger,
    fmt='%(asctime)s - %(levelname)s - %(message)s'
)

# File Handler
file_handler = logging.FileHandler(f"{log_folder}/app.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Only if there are no handlers
if not logger.hasHandlers():
    logger.addHandler(file_handler)

# Werkzeug Noise Silencing
logging.getLogger("wekzeug").setLevel(logging.WARNING)