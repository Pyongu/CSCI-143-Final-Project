import os

from flask import Flask, jsonify, send_from_directory, request, render_template, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import sqlalchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

# create database connection
engine = sqlalchemy.create_engine("postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev", connect_args={
    'application_name': '__init__.py root()',
    })
connection = engine.connect()

def are_credentials_good(username, password):
    with connection.begin() as trans:
        sql=sqlalchemy.sql.text('''
        SELECT count(*)
        FROM users
        where
            username = :username AND
            password = :password
        ''')

        res = connection.execute(sql, {
            'username':username,
            'password':password
            })
    if res.scalar() == 1:
        return True
    else:
        return False

def account_create_good(username, password1, password2):
    with connection.begin() as trans:
        sql=sqlalchemy.sql.text('''
        INSERT INTO users (
        username,
        password
        ) VALUES (
        :username,
        :password
        )''')

        try:
            res = connection.execute(sql, {
                'username': username,
                'password': password1
            })
            return True
        except sqlalchemy.exc.IntegrityError:
            return False


@app.route("/")
def root():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    gc = are_credentials_good(username, password)
    return render_template('root.html', logged_in=gc)

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    gc = are_credentials_good(username, password)
    # this firstLogin thing is not working
    firstLogin = ((username==None and password==None) or (username=='' and password==''))
    if gc and firstLogin:
        return render_template('login.html', logged_in=False, bad_credentials=False)
    elif gc and not firstLogin:
        #template = render_template('login.html', logged_in=True, bad_credentials=False)
        response = make_response(redirect('/'))
        response.set_cookie('username', username)
        response.set_cookie('password', password)
        return response
    else:
        return render_template('login.html', logged_in=False, bad_credentials=True)

@app.route("/logout")
def logout():
    # Not sure where this should redirect too
    response = make_response(redirect('/'))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    passDiff = (password1 != password2)
    accountMade = account_create_good(username, password1, password2)
    # Fixed Error Message Bug
    if passDiff: 
        return render_template('create_account.html', diff_password=True)
    elif accountMade: 
        response = make_response(redirect('/'))
        response.set_cookie('username', username)
        response.set_cookie('password', password1)
        return response
        # return render_template('create_account.html', diff_password=False, account_exists=False)
    else:
        return render_template('create_account.html', diff_password=False, account_exists=True)

@app.route("/create_message")
def create_message():
    return render_template('create_message.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
