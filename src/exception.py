import sys  # Import the sys module to interact with the Python runtime environment
from src.logger import logging  # Import the logging object from the src.logger module for logging purposes

def error_message_detail(error, error_detail: sys):
    """
    Generates a detailed error message including the file name and line number where the error occurred.

    Parameters:
    - error: The exception instance that was raised.
    - error_detail (sys): The sys module to access exception information.

    Returns:
    - A formatted string containing detailed error information.
    """
    # Retrieve exception type, value, and traceback from the current exception context
    _, _, exc_tb = error_detail.exc_info()
    
    # print (f"error detail :{error_detail.exc_info()}")
    
    # Extract the filename where the exception occurred from the traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename

    # print (f"exe_tb :{exc_tb.tb_frame}")
    
    # Extract the line number in the file where the exception occurred
    line_number = exc_tb.tb_lineno
    
    # Convert the error message to a string
    error_str = str(error)
    
    # Create a detailed error message with filename, line number, and the error message
    error_message = (
        "Error occurred in python script name [{0}] "
        "line number [{1}] error message [{2}]"
    ).format(file_name, line_number, error_str)
    
    return error_message  # Return the formatted error message

class CustomException(Exception):
    """
    A custom exception class that extends the built-in Exception class.
    It provides a detailed error message including the file name and line number.
    """
    
    def __init__(self, error_message, error_detail: sys):
        """
        Initializes the CustomException instance with a detailed error message.

        Parameters:
        - error_message: The original error message or exception.
        - error_detail (sys): The sys module to access exception information.
        """
        # super().__init__(error_message)  # Initialize the base Exception with the original error message

        # Generate a detailed error message using the error_message_detail function
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        print("\n\n+++++++++++++++++++++",self.error_message, "\n\n+++++++++++++++++++++")
        
    def __str__(self):
        """
        Python tries to log the object msg. To do this, it first needs to convert the msg 
        object into a string (since log messages are always strings).
        
        The logging module internally calls str(msg).
        When str(msg) is called, Python looks for the __str__() method in the CustomException class 
        and calls it. str(msg) not going typing using default string conversion.  

        __str__(): The __str__() method, on the other hand, is specifically designed to define what should be 
        returned when an object is converted to a string (e.g., when you print it). 
        
        
        """
        return self.error_message  # Return the detailed error message when the exception is printed


# try :
#     a=10
#     b=a/0
# except Exception as e:
#     msg =CustomException(e, sys)

#     """
#     Python tries to log the object msg. To do this, 
#     it first needs to convert the msg object into a string (since log messages are always strings)
#
#     """
#     logging.info(msg) # Message we are logging, we got that from __str__() methods return. 
    