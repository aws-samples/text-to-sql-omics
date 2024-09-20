import logging
import inspect

# Create a custom formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Get the file name, method name, and line number
        file_name = record.filename
        method_name = record.funcName
        line_number = record.lineno

        # Format the log message
        log_message = f"[{record.levelname}] ({file_name}|{method_name}:{line_number}): {record.getMessage()} "

        return log_message

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set the custom formatter
console_handler = logging.StreamHandler()
formatter = CustomFormatter()
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)
