import os
from flask import Flask, url_for, flash, request, redirect
from flask import render_template, session
from werkzeug.utils import secure_filename
from markupsafe import Markup
import secrets
from db_functions import execute_external_script, get_row_count_table, updatepassword
from db_functions import run_search_query, generateHTMLtable
from db_functions import reformatSQLiteDate


db_path = 'data/data.sqlite'


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt' , 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.globals.update(reformatSQLiteDate=reformatSQLiteDate)

app.secret_key = secrets.token_hex()

def new_lines_paragraph(s):
    new_str = "<p>" + s.replace("\n", "</p><p>") + "</p>"
    return Markup(new_str)

app.jinja_env.globals.update(new_lines_paragraph=new_lines_paragraph)



def validate_name(name):
    if len(name)<2:
        return False
    else:
        return True


def allowed_file(file):
    print(str(file))
    filename = file.filename
    if '.' in filename:
        extension = filename.rsplit('.',1)[1].lower()
        if extension in ALLOWED_EXTENSIONS:
            return secrets.token_hex()+'.'+extension
        else:
            return None
    else:
        return None



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #needs a session
        f= request.files['file']
        if f:
            filename = allowed_file(f)
            if filename:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return "<h1>A file is recognised and has been posted</h1>"
            else:
                return "<h1>File structure not recognised</h1>"
        else:
            return "<h1>No file here</h1>"
    else:
        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



@app.route('/login', methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        if validate_name(name):
            session['username'] = name
            return redirect( url_for('index') )
        else:
            return render_template('log-in.html', nameerror="Name Error")
    else:
        return render_template('log-in.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect( url_for('index') )




# decorated functions
@app.route('/')
def  index():
    sql = "select title, body, created_at, id from post"
    result = run_search_query(sql, db_path)
    return render_template('index.html', posts=result)

@app.route('/viewpost/<post_id>')
def viewpost(post_id):
    return "<h1> Viewpost </h1>"


@app.route('/installer' , methods=['GET','POST'])
def installer():
    """Delete all tables and re build initial database"""
    #initialisation script
    sql_script_path = 'data/init.sql'
    # page with button to install
    if request.method == 'GET':
        return render_template('installer.html', method="GET")
    elif request.method =='POST':
        global db_path
        # special call for external script
        if execute_external_script(sql_script_path, db_path):
            # data base has been rebuilt
            # now create new hashed password
            pword = updatepassword('admin',db_path)
            #organise feedback data
            row_data = dict()
            for t in ['post', 'comment','user']:
                row_data["Table: "+t] = "Number of Rows= "+str(get_row_count_table(t,db_path))
            row_data["New Password: "] = pword
            return render_template('installer.html', method="POST", row_data=row_data)
        else:
            return "<h1> Page Error on POST </h1>"

    else:
        return "<h1> Page Error </h1>"

@app.route('/viewtable/<tablename>')
def viewtable(tablename):
    """Create HTML table of database table data and render on page

    :param (str) tablename:
    :return: (html) render_template
    """
    global db_path
    if tablename == "master-data":
        sql = 'select * from sqlite_master;'
        result = run_search_query(sql, db_path)
        tablelisting = generateHTMLtable(result[1:], result[0])
        return render_template('table-data.html', tablelisting = Markup(tablelisting))
    elif tablename in ['post', 'comment', 'user']:
        headings={
            'user' : ('id','username', 'password', 'created_at', 'is_enabled' ),
            'post' : ('id', 'title', 'body', 'user_id', 'created_at','updated_at' ),
            'comment' : ('id', 'post_id', 'created_at', 'name', 'website', 'text')
        }
        sql = 'select * from {};'.format(tablename)
        result = run_search_query(sql, db_path)
        tablelisting = generateHTMLtable(result , headings[tablename])
        return render_template('table-data.html', tablelisting=Markup(tablelisting))
    else:
        return "<h1> Table not found </h1>"



with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login',next = '6'))



if __name__ == "__main__":
    app.run(debug=True)
