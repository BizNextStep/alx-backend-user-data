#!/usr/bin/env python3
"""
Module for creating a logger that redacts PII in log messages and connecting to a secure database.
"""

import logging
import os
import mysql.connector
from mysql.connector import Error
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger that redacts PII in log messages.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to a secure database using credentials from environment variables.
    Returns a MySQLConnection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    try:
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        if connection.is_connected():
            return connection
    except Error as e:
        logger = get_logger()
        logger.error(f"Error connecting to database: {e}")
        return None


def main():
    """
    Main function to retrieve and log user data from the database.
    """
    logger = get_logger()
    db = get_db()
    if db is None:
        logger.error("Failed to connect to the database.")
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    for row in rows:
        # Prepare the log message
        log_message = "; ".join(f"{key}={value}" for key, value in row.items())
        # Log the filtered message
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
