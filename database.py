'''
Author: Fabio Okubo
Date: 8/7/2020
version: 1
Description:
    Week 7 programming assignment 
    functions to help with database operations
'''

import sqlite3

def create_table(db_name, table_name, table_headers):
    ''' create table in database with headers
        arg1 database name, arg2 table name, 
        arg3 table headers are strings separated by commas
    '''
    try:
        #connect to a database
        conn = sqlite3.connect(db_name)

        #create a cursor
        c = conn.cursor()

        #if table already exists drop table
        c.execute("DROP TABLE IF EXISTS " + table_name)
        #create table
        c.execute("CREATE TABLE " + table_name + "(" + table_headers + ")")
        #commit changes to db
        conn.commit()
    except:
        print("Table " + table_name + " already exist...")
    finally:
        #close db
        conn.close()


def create_mask(items):
    '''Mask used to allow add_one function to accommodate 
        other sizes of lists '''
    mask = "("

    for i in range(len(items)):
        mask += "?,"

    #remove last comma and add closing parenthesis
    mask = mask[:-1] + ")"

    return mask


def add_one(db_name, table_name, content):
    ''' add on record to table '''
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        arg = "INSERT INTO " + table_name + " VALUES " + create_mask(content)
        c.execute(arg, content)
        conn.commit()
    except:
        print("Error adding one record to table")
    finally:
        conn.close()

def get_selected_data(db_name, table_name, columns):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT " + columns + " FROM " + table_name)
        items = c.fetchall()
        conn.close()  
        return items   
    except:
        print("Error retrieving data")
    finally:
        conn.close()        

        

def show_all(db_name, table_name):
    '''print data from table to screen'''

    try:
        #connect to a database
        conn = sqlite3.connect(db_name)

        #create a cursor
        c = conn.cursor()

        c.execute("SELECT * FROM " + table_name)
        items = c.fetchall()

        for item in items:
            print(item)

    except:
        print("Error printing records")
    finally:
        conn.close()          