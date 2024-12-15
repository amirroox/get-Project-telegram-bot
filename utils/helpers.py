import smtplib
import ssl
from email.message import EmailMessage
from utils import config

from contextlib import contextmanager

import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from typing import Union


# Connection Pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    user=config.DATABASE_USER,
    password=config.DATABASE_PASS,
    database=config.DATABASE_NAME,
    autocommit=True
)


# Create a connection DB
@contextmanager
def create_connection() -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    connection = None
    try:
        connection = connection_pool.get_connection()
        yield connection
    except mysql.connector.Error as err:
        print(f"Error in DB: {err}")
        raise
    finally:
        if connection:
            connection.close()


# Send Mail Func
def send_mail(subject, text):
    port = config.MAIL['port']
    smtp_server = config.MAIL['server']
    sender_email = config.MAIL['sender']
    receiver_email = config.MAIL['receiver']
    password = config.MAIL['password']

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(text)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)

    except Exception as er:
        print('Error Send Mail: ', er)
        raise Exception

