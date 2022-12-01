import os
import sqlite3
from _datetime import datetime
import random
import hashlib

def pythondateNow_toSQLiteDate():
    x = datetime.now()
    y = x.strftime('%Y-%m-%d %H:%M:%S')
    return y

def reformatSQLiteDate(sqlite_datestring):
    """Reformat SQLite date to d-m-y

    :param (str) sqlite_datestring:
    :return: (str) date
    """
    x = datetime.strptime(sqlite_datestring, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%d/%m/%Y")



def create_pword_hash(length=10):
    """Create a new random password and hash

    :param (int) length:
    :return: (tuple) password, hash
    """
    pword = ""
    for x in range(0, length):
        # randomly select characters A through Z
        pword += chr(random.randint(ord('A'),ord('Z')))
    h = hashlib.md5(pword.encode())
    hash = h.hexdigest()
    return pword , hash

def get_password_hash(password):
    h = hashlib.md5(password.encode())
    hash = h.hexdigest()
    return hash


def updatepassword(user_id, db_path, password='temp'):
    """Create a new password with hash and update db"

    :param (str) user_id:
    :param (path) db_path:
    :return: (str) password
    """
    sql = """
    update user 
    set password = ?, created_at = ?
    where user_id = ?
    """
    #password, hash = create_pword_hash()
    hash = get_password_hash(password)
    created_at = pythondateNow_toSQLiteDate()
    values_tuple = (hash, created_at, user_id)
    run_commit_query(sql, values_tuple, db_path)
    return password

def check_password(pword, hash):
    """Compare password given with a hash value

    :param (str) pword:
    :param (str) hash:
    :return: (bool) True if it is a match
    """
    h = hashlib.md5(pword.encode())
    if hash == h.hexdigest():
        return True
    else:
        return False

def generateHTMLtable(result_tuple_list, header_tuple=()):
    """Create HTML formatted table

    :param (list(tuple)) result_tuple_list:
    :param (tuple_ header_tuple:
    :return: (str) tablestring
    """
    if result_tuple_list is None:
        return "<table></table>"
    tablestring="<table><tr>"
    if len(header_tuple) >0:
        for cell in header_tuple:
            tablestring += "<th> {} </th>".format(cell)
        tablestring += "</tr>\n<tr>"
    for row in result_tuple_list:
        for cell in row:
            tablestring+="<td> {} </td>".format(cell)
        tablestring +="</tr>\n<tr>"
    tablestring += "</tr></table>"
    return tablestring


#absolute_db_path = os.path.abspath(db_path)

def run_commit_query(sql_query,values_tuple, file_path):
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        print("connection successful")
        cursor.execute(sql_query, values_tuple)
        conn.commit()
        print("Commit Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Commit Error: {}".format(error))
    finally:
        if conn:
            conn.close()
            print("sqlite connection is closed")

def run_search_query(sql_query, file_path):
    """Run a Query only

    :param (str) sql_query:
    :param (path) file_path:
    :return: (tuple) result
    """
    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        #db.row_factory = sql.Row
        cursor = db.cursor()
        #print("connection successful")
        cursor.execute(sql_query)
        result = cursor.fetchall()
        #print("Search Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while creating sqlite table: {}".format(error))
    finally:
        if db:
            db.close()
            #print("sqlite connection is closed")
        if result:
            return result

def run_search_query_tuples(sql_query,values_tuple, file_path):
    """Run a Query only

    :param (str) sql_query:
    :param (path) file_path:
    :return: (tuple) result
    """
    result = None
    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        #db.row_factory = sql.Row
        cursor = db.cursor()
        #print("connection successful")
        cursor.execute(sql_query,values_tuple)
        result = cursor.fetchall()
        #print("Search Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error running search query tuples: {}".format(error))
    finally:
        if db:
            db.close()
            #print("sqlite connection is closed")
        if result:
            return result

def execute_external_script(sql_script_path, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        #print("connection successful")
        sql_query = open(sql_script_path)
        sql_string = sql_query.read()
        cursor.executescript(sql_string)
        conn.commit()
        #print("Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while executing sql: {}".format(error))
        return False
    finally:
        if conn:
            conn.close()
            return True
            #print("sqlite connection is closed")

def get_row_count_table(tablename,db_path):
    sql = "select count(*) as c from {}".format(tablename)
    result= run_search_query(sql,db_path)
    return result[0][0]




if __name__ == "__main__":
    db_path = 'data/data.sqlite'
    sql_script_path = 'data/init.sql'
    print(os.path.abspath(db_path))
    ['1', '2', '3', '4']










