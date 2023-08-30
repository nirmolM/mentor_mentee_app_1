import mysql.connector
from working_data import password_giver as pg
"""
Possible Errors:
1. localhost login error 10061, MEANS SERVICE not running
-> To remove error, go to start, search for services, search for MySQL and then enable it, or run it
"""


def make_connection():
    """This will make a connection without SELECTING a DATABASE
    This is used to Make, Show and Remove Database"""
    connection = mysql.connector.connect(user='root', password=pg.give_password(), host='localhost', buffered=True)
    return connection


def show_databases():
    """This will show Existing databases RELEVANT to the APP"""
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute("SHOW DATABASES")
    cursor_local.close()
    connection_local.close()
    database_list = [databases[0] for databases in cursor_local]
    to_remove = ['information_schema', 'mysql', 'performance_schema', 'sakila', 'sys', 'world']
    database_list_to_return = [db for db in database_list if db not in to_remove]
    return database_list_to_return


def create_database(db_name: str):
    """Will Create a new database, with the name given in argument"""
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"CREATE DATABASE {db_name}")
    cursor_local.close()
    connection_local.close()


def delete_database(db_name: str):
    """Will Delete a database, with the name given in argument"""
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"DROP DATABASE {db_name}")
    cursor_local.close()
    connection_local.close()
