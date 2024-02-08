#!/usr/bin/env python3
"""
Module for filtered logging functionalities.
"""
import logging
import re
import os
import mysql.connector
from typing import List, Tuple


PII_FIELDS = ("email", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum.

        Args:
            record: The LogRecord to be formatted.

        Returns:
            str: The formatted log message.
        """
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_message, self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message using regex.

    Args:
        fields: A list of strings representing fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all fields in the log line.

    Returns:
        str: The filtered log message with specified fields obfuscated.
    """
    return re.sub(
        '|'.join(f'(?<={separator}|^){field}=[^{separator}]*' for field in fields),
        lambda match: f"{match.group().split('=')[0]}={redaction}",
        message
    )

def get_logger() -> logging.Logger:
    """
    Creates a logging.Logger object.

    Returns:
        logging.Logger: The created logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The connector to the MySQL database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

def main() -> None:
    """
    Retrieves all rows in the users table, filters the data, and displays each row.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        filtered_row = {field: "***" if field in PII_FIELDS else row[field] for field in row}
        print(f"[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: {filtered_row};\nFiltered fields:\n{name}\n{email}\n{phone}\n{ssn}\n{password}\n")
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
