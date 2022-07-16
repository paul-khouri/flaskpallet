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


def updatepassword(username, db_path):
    """Create a new password with hash and update db"

    :param (str) username:
    :param (path) db_path:
    :return: (str) password
    """
    sql = """
    update user 
    set password = ?, created_at = ?, is_enabled = 0
    where username = ?
    """
    password, hash = create_pword_hash()
    created_at = pythondateNow_toSQLiteDate()
    values_tuple = (hash, created_at, username)
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
    :return: (str) tablestaring
    """
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





def set_one(db_path):
    result = get_row_count_table('post', db_path)
    print(result)
    sql = "select count(*) as c from post"
    result = run_search_query(sql, db_path)
    print(result)
    sql = "select * from post"
    result = run_search_query(sql, db_path)
    print(result)
    for x in result:
        for y in x:
            print(y)
    sql = 'select * from sqlite_master;'
    result = run_search_query(sql, db_path)
    # for x in result:
    # print(x)
    sql = "select id, title, created_at, body,(select count(*) from comment " \
          "where comment.post_id = post.id) comment_count " \
          "from post order by created_at desc"
    result = run_search_query(sql, db_path)
    print(result)

def set_two(db_path):
    sql = "select * from user"
    result = run_search_query(sql, db_path)
    print(result)
    # updatepassword('admin', db_path)
    sql = "insert into user (username, password, created_at, is_enabled)" \
          "values ('test', 'sdjjsdg', '2021-09-28 16:50:48', 0)"
    run_commit_query(sql, (), db_path)
    sql = "insert into user (username, password, created_at, is_enabled)" \
          "values (?, ?, ?, ?)"
    run_commit_query(sql, ('qtest', 'aaa', '2021-09-28 16:50:48', 0), db_path)
    sql = "select * from user"
    result = run_search_query(sql, db_path)
    print(result)
    sql = "delete from user where id>1"
    run_commit_query(sql, (), db_path)
    sql = "select * from user"
    result = run_search_query(sql, db_path)
    print(result)

def set_three(db_path):
    sql = """
        update user 
        set password = 'lavatsa', created_at = '2021-09-28 16:50:48', is_enabled = 1
        where username = 'admin' 
        """
    run_commit_query(sql, (), db_path)
    sql = "select * from user"
    result = run_search_query(sql, db_path)
    print(result)
    sql = """
        update user 
        set password = ?, created_at = ?, is_enabled = 0
        where username = ?
        """
    values_tuple = ('maya', '1800-09-28 16:50:48', 'admin')
    password, hash = create_pword_hash()
    created_at = pythondateNow_toSQLiteDate()
    values_tuple = (hash, created_at, 'admin')
    run_commit_query(sql, values_tuple, db_path)
    sql = "select * from user"
    result = run_search_query(sql, db_path)
    print(result)




if __name__ == "__main__":
    db_path = 'data/data.sqlite'
    sql_script_path = 'data/init.sql'
    #execute_external_script(sql_script_path, db_path)
    #set_one(db_path)
    #set_two(db_path)
    #set_three(db_path)
    #print(updatepassword('admin', db_path))
    # sql = "select * from user"
    # field_list = ('id', 'username', 'password', 'created_at', 'is_enabled')
    # result = run_search_query(sql, db_path)
    # print(result)
    # sql = 'select * from sqlite_master;'
    # result = run_search_query(sql, db_path)
    # #print(result)
    # table = generateHTMLtable(result[1:], result[0])
    # print(table)









