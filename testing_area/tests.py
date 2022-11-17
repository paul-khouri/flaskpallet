import secrets

import sys
import os
import db_functions
from db_functions import run_search_query
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(SCRIPT_DIR)
sys.path.append(os.path.dirname(SCRIPT_DIR))



file_string="hello.jpg"
ALLOWED_EXTENSIONS = {'txt' , 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    if '.' in filename:
        extension = filename.rsplit('.',1)[1].lower()
        if extension in ALLOWED_EXTENSIONS:
            return secrets.token_hex()+'.'+extension
        else:
            return None
    else:
        return None

#print(allowed_file(file_string))

def test_linelength():

    db_path = '../data/data.sqlite'
    sql = "select title, substr(body, 0,160), created_at, id, image, alttext from post order by created_at desc;"
    blog_result = run_search_query(sql, db_path)
    print(blog_result)

#test_linelength()

def check_user():
    db_path = '../data/data.sqlite'
    sql = "select * from user"
    blog_result = run_search_query(sql, db_path)
    print(blog_result)

check_user()

