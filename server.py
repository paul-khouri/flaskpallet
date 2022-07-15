import os
from flask import Flask, url_for, flash, request, redirect
from flask import render_template, session
from werkzeug.utils import secure_filename
from markupsafe import Markup
import secrets
from db_functions import execute_external_script, get_row_count_table, updatepassword
from db_functions import run_search_query, generateHTMLtable, run_search_query_tuples, run_commit_query
from db_functions import reformatSQLiteDate, pythondateNow_toSQLiteDate
from flask import g



db_path = 'data/data.sqlite'


UPLOAD_FOLDER = 'static/uploadedimages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
                img_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(img_path)
                files = os.listdir(app.config['UPLOAD_FOLDER'])
                return render_template('upload.html', message="A file has been recognised and posted",  latest_file=filename)
            else:
                return render_template('upload.html', message="File not recognised")
        else:
            return render_template('upload.html', message="There is no file")
    else:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        print(files)
        print(app.config['UPLOAD_FOLDER'])
        return render_template('upload.html', files=files)



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
    blog_result = run_search_query(sql, db_path)
    return render_template('index.html', posts=blog_result)

@app.route('/viewpost/<post_id>')
def viewpost(post_id):
    sql="select title, body, created_at, id from post where id= ?"
    values_tuple= tuple(post_id)
    result= run_search_query_tuples(sql,values_tuple,db_path)
    post_tuple = result[0]
    session['post_data']=post_tuple
    sql="select name, text, website, created_at from comment where post_id= ?"
    values_tuple= tuple(post_id)
    result = run_search_query_tuples(sql, values_tuple, db_path)
    print(result)
    return render_template('viewposts.html',post_id=post_id, post=post_tuple, comments=result)

@app.route('/editpost/<post_id>', methods=['GET','POST'])
def editpost(post_id):
    if request.method =='POST':
        title = request.form['title']
        content = request.form['content']
        sql="""
        UPDATE
        post
        SET
        title = ?, body = ?, updated_at = ?
        WHERE
        id = ?;
        """
        updated_at = pythondateNow_toSQLiteDate()
        update_tuple=(title,content,updated_at,post_id)
        run_commit_query(sql, update_tuple,db_path)
        return redirect( url_for('viewpost', post_id = post_id) )
    else:
        return render_template('editpost.html',post_id=post_id, title=session['post_data'][0], content=session['post_data'][1])

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
