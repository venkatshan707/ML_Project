# Import the logging module to handle logging operations in Python.
import logging

# Import the os module to interact with the operating system for file path manipulation and directory creation.
import os

# Import the datetime class from the datetime module to handle date and time, which is used to generate unique log file names.
from datetime import datetime

# Create a string representing the log file name.
# The file name is generated using the current date and time in the format: month_day_year_hour_minute_second.
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the full path for the logs directory and the log file inside it.
# os.getcwd() gets the current working directory, and os.path.join() joins the paths to create the full path.
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the logs directory if it doesn't already exist.
# os.makedirs() ensures that the directory is created, and exist_ok=True prevents an error if the directory already exists.
os.makedirs(logs_path, exist_ok=True)

# Construct the full path for the log file, including the directory path and the log file name.
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the logging system.
# - filename: Specifies the path to the log file.
# - format: Specifies the log format, including timestamp, line number, module name, log level, and the log message.
# - level: Sets the log level to INFO, meaning it will log all messages at INFO level and above (INFO, WARNING, ERROR, etc.).
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Path to the log file
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Log message format
    level=logging.INFO,  # Logging level set to INFO
)

if __name__ == "__main__":
    logging.info("Logging started.")