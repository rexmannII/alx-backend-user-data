#!/usr/bin/env python3


import re
import logging
import os
import mysql.connector
from mysql.connector import Error


# PII fields defined here
PII_FIELDS = ("email", "password", "ssn", "phone_number", "address")

def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the values of the specified fields in a log message using regex.
    
    Args:
        fields (list): A list of fields to obfuscate.
        redaction (str): The string to replace field values with.
        message (str): The log message to be processed.
        separator (str): The character that separates fields in the log message.
    
    Returns:
        str: The obfuscated log message.
    """
    return re.sub(r'(' + '|'.join([re.escape(field) for field in fields]) + r')=[^' + re.escape(separator) + r']*', r'\1=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        """
        Initialize the RedactingFormatter with a list of fields to redact.
        
        Args:
            fields (list): A list of field names (e.g., ["email", "ssn", "password"]) to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
        """
        Format the log record by redacting the specified fields in the message.
        
        Args:
            record (logging.LogRecord): The log record to be formatted.
        
        Returns:
            str: The formatted log message with redacted fields.
        """
        record.message = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

    
    
def get_logger() -> logging.Logger:
        """
        Returns a logger named 'user_data' with a StreamHandler that uses RedactingFormatter.
        The logger will only log messages at INFO level or higher, and will not propagate messages.
        """
        logger = logging.getLogger("user_data")
        logger.setLevel(logging.INFO) # Only log messages at INFO level aor higher
        logger.propagate = False # Prevent log messages from propagating to other loggers

        # Set up the handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

        # Add the handler to the logger
        logger.addHandler(stream_handler)

        return logger
