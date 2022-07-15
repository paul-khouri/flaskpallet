import os
from flask import Flask, url_for, flash, request, redirect
from flask import render_template, session
from werkzeug.utils import secure_filename
from markupsafe import Markup
import secrets
from db_functions import destory_re_init_db

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt' , 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = secrets.token_hex()


# regular functions
def get_current_pages():
    page_set =[(url_for('index'), "index"),
     (url_for('login'), "log-in"),
     (url_for('login',next = '6'), "log-in with query"),
     (url_for('profile', username="Paul Khouri"), "profile")
     ]
    return page_set

def get_safe_table():
    table = "<table>\n<tr>"
    for x in range(1, 101):
        table += "<td> {} </td>".format(x)
        if x!= 100 and x%10==0:
            table += "</tr>\n<tr>"
    table += "</tr>\n</table>"
    print(table)
    return Markup(table)

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

# decorated functions
@app.route('/')
def  index():
    return render_template('index.html')

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

@app.route('/details')
def details():
    table = get_safe_table()
    name = "Michael"
    navigation = get_current_pages()
    return render_template('details.html',
                           table=table,
                           navigation=navigation,
                           name=name)

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


@app.route('/user/<username>')
def profile(username):
    return f"<p> Hello, {username}!</p>"

@app.route('/installer' , methods=['GET','POST'])
def installer():
    return render_template('installer.html')


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login',next = '6'))
    print(url_for('profile', username="Paul Khouri"))


if __name__ == "__main__":
    app.run(debug=True)
