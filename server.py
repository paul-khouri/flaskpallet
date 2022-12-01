import os
import re
from flask import Flask, url_for, request, redirect
from flask import render_template, session
from markupsafe import Markup
import secrets
from db_functions import execute_external_script, get_row_count_table, updatepassword, get_password_hash
from db_functions import run_search_query, generateHTMLtable, run_search_query_tuples, run_commit_query
from db_functions import reformatSQLiteDate, pythondateNow_toSQLiteDate

sql_script_path = 'data/init.sql'
db_path = 'data/data.sqlite'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = secrets.token_hex()

# ---- functions that can be used on template pages
app.jinja_env.globals.update(reformatSQLiteDate=reformatSQLiteDate)


def new_lines_paragraph(s):
    new_str = "<p>" + s.replace("\n", "</p><p>") + "</p>"
    return Markup(new_str)


app.jinja_env.globals.update(new_lines_paragraph=new_lines_paragraph)
# ----------------------------------------------------


def validate_name(name, password="a"):
    """check that a user name and password is correct

    :param (str) name
    :param (str) password
    :return (int) id
    """
    sql = """select user_id,password, permission from user where username=?"""
    # get the hash of the password
    hashed_password = get_password_hash(password)
    # stripped name for search
    name_tuple = (name.lower().strip(),)
    print(name_tuple)
    result = run_search_query_tuples(sql, name_tuple, db_path)
    if result:
        if result[0][1] == hashed_password:
            return result[0][0], result[0][2]
        else:
            return None, None
    else:
        return None, None


def session_check(permission):
    """Check if user has permission to access the page

    :param permission: (int)
    :return: boolean
    """
    if session:
        if session['permission'] > permission:
            return False
        else:
            return True
    else:
        return False


def allowedpost(post_id):
    """Check if if user is allowed to endit/delete a post

    :param post_id: str
    :return:
    """
    if post_id in session['ownedposts']:
        return True
    elif session['permission'] == 0:
        # admin has full access
        return True
    else:
        return False

def update_owned_posts():
    """Update session variable with all post-ids that
    belong to the logged in user

    :return: None
    """
    sql = "select post_id from post where user_id=?"
    values_tuple = (session['id'],)
    result = run_search_query_tuples(sql, values_tuple, db_path)
    session['ownedposts'] = re.findall(r"[0-9]+", str(result))


@app.route('/login', methods=['GET', 'POST'])
def login():
    global db_path
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        check, permission = validate_name(name, password)
        if check:
            session['username'] = name
            session['id'] = check
            session['permission'] = permission
            update_owned_posts()
            # if all okay, go to index
            return redirect(url_for('index'))
        else:
            return render_template('log-in.html', nameerror="Log-in name not recognised")
    else:
        return render_template('log-in.html', namevalue="admin", password="")


@app.route('/logout')
def logout():
    # delete all session keys
    session.clear()
    # go to index
    return redirect(url_for('index'))


@app.route('/')
def index():
    # get all posts with truncated text
    sql = "select title, substr(body, 0,300), created_at, post_id, image, alttext from post order by created_at desc;"
    blog_result = run_search_query(sql, db_path)
    if blog_result:
        return render_template('index.html', posts=blog_result)
    else:
        # if no results (None)
        return render_template('index.html')


@app.route('/viewpost/<post_id>', methods=['GET','POST'])
def viewpost(post_id):
    global db_path
    # get the post with the user name
    sql = """select post.title, post.body, post.created_at, post.image, post.alttext, post.user_id, user.username from post 
                join user on post.user_id = user.user_id
                where post.post_id= ?"""

    # convert post_id str to tuple
    values_tuple = tuple(post_id)
    result = run_search_query_tuples(sql, values_tuple, db_path)
    post_tuple = result[0]
    if post_tuple is None:
        error = "Unfortunately something has gone wrong and we cannot find the post you are looking for"
        return render_template("error.html", error=error)
    # complete another database request for the specific post
    sql = """select comment.user_id, comment.text, comment.created_at, user.username from comment 
              join user on comment.user_id=user.user_id
                  where comment.post_id= ?"""
    values_tuple = tuple(post_id)
    result = run_search_query_tuples(sql, values_tuple, db_path)
    if request.method == "GET":
        return render_template('viewposts.html', post_id=post_id, post=post_tuple, comments=result)
    elif request.method == "POST":
        # add comments to db
        comment = request.form['Comment Text']
        user_id = session['id']
        sql = """insert into comment(post_id, created_at, user_id, text) values(?,?,?,?);"""
        values_tuple = (post_id,pythondateNow_toSQLiteDate(), user_id, comment )
        run_commit_query(sql, values_tuple,db_path)
        # re query comments with new one added -- fix so name is queried as well
        sql = "select user_id, text, created_at from comment where post_id= ?"
        values_tuple = tuple(post_id)
        result = run_search_query_tuples(sql, values_tuple, db_path)
        return render_template('viewposts.html', post_id=post_id, post=post_tuple, comments=result)



@app.route('/deletepost/<post_id>', methods=['GET', 'POST'])
def deletepost(post_id):
    description = request.args.get('description', None)
    if not session_check(1) or not allowedpost(post_id):
        error = "You do not have permission to view this page"
        return render_template('error.html', error=error)
    global db_path
    if request.method == 'GET':
        return render_template("confirmation.html", description=description, post_id=post_id)
    elif request.method == 'POST':
        # delete all comments
        sql="delete from comment where post_id = ?"
        values_tuple = tuple(post_id)
        run_commit_query(sql, values_tuple, db_path)
        # delete post
        sql="delete from post where post_id = ?"
        values_tuple = tuple(post_id)
        run_commit_query(sql, values_tuple, db_path)
        update_owned_posts()
        return redirect(url_for('index'))

# ----   edit post and new post substantial consolidating (maybe)     -------------
@app.route('/editpost/<post_id>', methods=['GET', 'POST'])
def editpost(post_id):
    if not session_check(1) or not allowedpost(post_id):
        error = "You do not have permission to view this page"
        return render_template('error.html', error=error)
    sql = "select title, body, created_at, image from post where post_id= ?"
    values_tuple = tuple(post_id)
    result = run_search_query_tuples(sql, values_tuple, db_path)
    post_tuple = result[0]
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        f = request.files['file']
        if f.filename == "":
            sql = """
            UPDATE
            post
            SET
            title = ?, body = ?, updated_at = ?
            WHERE
            post_id = ?;
            """
            updated_at = pythondateNow_toSQLiteDate()
            update_tuple = (title, content, updated_at, post_id)
            run_commit_query(sql, update_tuple, db_path)
            return redirect(url_for('viewpost', post_id=post_id))
        elif f.content_type in ["image/jpeg", "image/png"]:
            sql = """
            UPDATE
            post
            SET
            title = ?, body = ?, updated_at = ?, image = ?, alttext =?
            WHERE
            post_id = ?;
            """
            # save the image to static
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            # prep tuple and run commit
            values_tuple = (title, content, pythondateNow_toSQLiteDate(), f.filename, "Image alt text", post_id)
            print(f.filename)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('viewpost', post_id=post_id))
        else:
            error = "You have chosen a file but it is not a correct type of file"
            return render_template('editpost.html', post_id=post_id, title=post_tuple[0],
                                   content=post_tuple[1], postimage=post_tuple[3], error=error)
    else:
        return render_template('editpost.html', post_id=post_id, title=post_tuple[0],
                               content=post_tuple[1], postimage=post_tuple[3])


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if not session_check(1):
        error = "You do not have permission to view this page"
        return render_template('error.html', error=error)
    if request.method == 'POST':
        # collect information from form using names in form
        title = request.form['title']
        content = request.form['content']
        f = request.files['file']
        # assess the image and feedback if problem
        # jpeg understands jpg
        if f.content_type in ["image/jpeg", "image/png"]:
            # if okay prep query
            sql = """
            insert into post(title, body, user_id, created_at,image, alttext) values(?,?,?,?,?,?);
            """
            # save the image to static
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            # prep tuple and run commit
            values_tuple = (title, content, session['id'], pythondateNow_toSQLiteDate(), f.filename, "Image alt text")
            run_commit_query(sql, values_tuple, db_path)
            update_owned_posts()
            return redirect(url_for('index'))
        elif f.filename == "":
            error = "You have not selected an image"
        else:
            error = "Image type not recognised"
        return render_template('newpost.html', entered_title=title, entered_content=content, error=error)
    else:
        return render_template('newpost.html', title="Name of book...", content="Passage from book...")


@app.route('/commentlist', methods=['GET','POST'])
def commentlist():
    global db_path
    if session['permission'] == 0:
        sql="select comment_id, text from comment"
        values_tuple =()
    else:
        sql = "select comment_id, text from comment where user_id=?"
        values_tuple=(session['id'],)
    result = run_search_query_tuples(sql,values_tuple,db_path)
    if result is None:
        result = {}
    if request.method == "GET":
        return render_template("commentslist.html", comments=result)
    elif request.method == "POST":
        to_delete = request.form
        nums= tuple(re.findall(r"[0-9]+", str(to_delete)))
        values_tuple_delete = ()
        sql_delete = "delete from comment where comment_id in {}".format(nums)
        run_commit_query(sql_delete, values_tuple_delete, db_path)
        result = run_search_query_tuples(sql, values_tuple, db_path)
        if result is None:
            result = {}
        return render_template("commentslist.html", comments=result)

# -------------- developer functions


@app.route('/installer', methods=['GET', 'POST'])
def installer():
    """Delete all tables and re build initial database"""
    #if not session_check(0):
        #error = "You do not have permission to view this page"
        #return render_template('error.html', error=error)
    # initialisation script
    global sql_script_path
    # page with button to install
    if request.method == 'GET':
        return render_template('installer.html', method="GET")
    elif request.method == 'POST':
        global db_path
        # special call for external script
        if execute_external_script(sql_script_path, db_path):
            # data base has been rebuilt
            # for summary print out
            row_data = dict()
            # get all users from the initialisation
            sql = "select user_id, username from user"
            users=run_search_query(sql,db_path)
            # loop and hash all passwords (defaults to temp)
            for u in users:
                row_data[u[1]]=updatepassword(u[0], db_path)
            # organise feedback data
            for t in ['post', 'comment', 'user']:
                row_data["Table: "+t] = "Number of Rows= "+str(get_row_count_table(t, db_path))
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
    if not session_check(0):
        error = "You do not have permission to view this page"
        return render_template('error.html', error=error)
    global db_path
    if tablename == "master-data":
        sql = 'select * from sqlite_master;'
        result = run_search_query(sql, db_path)
        tablelisting = generateHTMLtable(result[1:], result[0])
        return render_template('table-data.html', tablelisting=Markup(tablelisting))
    elif tablename in ['post', 'comment', 'user']:
        headings = {
            'user': ('user_id', 'username', 'password', 'created_at', 'permission'),
            'post': ('post_id', 'title', 'body', 'user_id', 'created_at', 'image', 'alttext', 'updated_at'),
            'comment': ('comment_id', 'post_id', 'created_at', 'user_id', 'text', 'updated_at')
        }
        sql = 'select * from {};'.format(tablename)
        result = run_search_query(sql, db_path)
        tablelisting = generateHTMLtable(result, headings[tablename])
        return render_template('table-data.html', tablelisting=Markup(tablelisting))
    else:
        return "<h1> Table not found </h1>"


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='6'))


if __name__ == "__main__":
    app.run(debug=True)
