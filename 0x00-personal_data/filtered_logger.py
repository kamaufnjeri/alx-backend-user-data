#!/usr/bin/env python3
"""Module for filtering sensitive information in logs."""
import os
import re
import logging
import mysql.connector
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
SENSITIVE_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_log_data(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters sensitive information in a log message."""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def initialize_logger() -> logging.Logger:
    """Creates a new logger for logging user data."""
    logger = logging.getLogger("user_data_logs")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(SENSITIVE_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def connect_to_database() -> mysql.connector.connection.MySQLConnection:
    """Establishes connection to a database."""
    db_host = os.getenv("SENSITIVE_DATA_DB_HOST", "localhost")
    db_name = os.getenv("SENSITIVE_DATA_DB_NAME", "")
    db_user = os.getenv("SENSITIVE_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("SENSITIVE_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """Logs information about user records from a database table."""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = initialize_logger()
    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = (
                "user_data_logs", logging.INFO, None, None, msg, None, None
            )
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class for log messages."""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record."""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_log_data(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == "__main__":
    main()
