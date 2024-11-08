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

    # Create a regex pattern that matches the field=value pairs
    pattern = r'(' + '|'.join([re.escape(field) for field in fields]) + r')=[^' + re.escape(separator) + r';]+'

    # Return matched patterns with the redaction string
    return re.sub(pattern, lambda  m: f'{m.group(1)}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class that filters specified fields in the log message."""

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

        # Store the fields to be redacted
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
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
        Create and configures a logger that filters PII data.
        
        
        Returns:
            logging.Logger: A configured logger.
        """

        # Create the logger with the name "user_data
        logger = logging.getLogger("user_data")

        # Set the Logging level to INFO
        logger.setLevel(logging.INFO)

        # Prevent messages from propagating to other loggers
        logger.propagate = False

        # Create a StreamHandler
        stream_handler = logging.StreamHandler()

        # Create an instance of the RedactingFormatter with PII_FIELDS
        formatter = RedactingFormatter(fields=PII_FIELDS)

        # Set the formatter to the StreamHandler
        stream_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(stream_handler)

        return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database using credentials from environment variables.

    
    Returns:
        mysql.connector.connection.MySQLConnection: A connection object to the database.
    

    Raises:
        Error: If there is an issue connecting to the database.
    """

    # Get database credentials from environment variables, with default if not set
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    if not db_name:
        raise ValueError("Database name must be specified in the environment variable PERSONAL_DATA_DB_NAME")


    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=db_name
        )

        if connection.is_connected():
            return connection
        else:
            raise Error("Failed to connect to the database.")

    except Error as e:
        print(f"Error: {e}")
        raise



def main() -> None:
    """
    Fetches user data from the database, filters the specified fields, 
    and logs the results using a logger.
    """
    # Get logger instance
    logger = get_logger()

    # Fetch data from the users table
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()

        # Log each row, filtering sensitive fields
        for row in rows:
            user_data = (
                f'name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; password={row[4]}; '
                f'ip={row[5]}; last_login={row[6]}; user_agent={row[7]};'
            )
            logger.info(user_data)

    except Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
