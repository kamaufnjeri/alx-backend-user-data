#!/usr/bin/env python3
"""
Module for handling sensitive data
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


SENSITIVE_FIELDS = ("name", "email", "phone", "ssn", "password")


def obfuscate_data(fields: List[str], redaction: str,
                   message: str, separator: str) -> str:
    """ Obfuscates sensitive data in a log message """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_secure_logger() -> logging.Logger:
    """ Returns a secure logger instance """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(SecureFormatter(list(SENSITIVE_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_secure_db_connector() -> mysql.connector.connection.MySQLConnection:
    """ Returns a secure connector to a MySQL database """
    username = environ.get("SENSITIVE_DATA_DB_USERNAME", "root")
    password = environ.get("SENSITIVE_DATA_DB_PASSWORD", "")
    host = environ.get("SENSITIVE_DATA_DB_HOST", "localhost")
    db_name = environ.get("SENSITIVE_DATA_DB_NAME")

    cnx = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host,
                                                     database=db_name)
    return cnx


def main():
    """
    Retrieves sensitive data from a database and logs it securely
    """
    db = get_secure_db_connector()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_secure_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


class SecureFormatter(logging.Formatter):
    """ Formatter class for secure logging """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(SecureFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using obfuscate_data """
        record.msg = obfuscate_data(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super(SecureFormatter, self).format(record)


if __name__ == '__main__':
    main()
