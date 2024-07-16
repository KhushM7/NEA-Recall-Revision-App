from __future__ import print_function
from typing import Dict

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

DB_NAME = "physics_revision_app"
TABLES: dict[str, str] = {
    "users": (
        "CREATE TABLE `users` ("
        "  `user_id` int NOT NULL AUTO_INCREMENT,"
        "  `username` varchar(50) NOT NULL,"
        "  `password` varchar(50) NOT NULL,"
        "  `email` varchar(50) NOT NULL,"
        "  PRIMARY KEY (`user_id`)"
        ") ENGINE=InnoDB"
    )
}

cnx = mysql.connector.connect(
    user="root",
    password="ne6$HQUfANzeA3b%",
    host="localhost",
    database="physics_revision_app",
)
cursor = cnx.cursor()


def create_database(db_cursor: MySQLCursorAbstract) -> None:
    try:
        db_cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as db_err:
        print("Failed creating database: {}".format(db_err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end="")
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
