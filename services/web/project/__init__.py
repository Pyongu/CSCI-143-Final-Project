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

# This function might not be needed
def username_exists(username):
    with connection.begin() as trans:
        sql=sqlalchemy.sql.text('''
        SELECT count(*)
        FROM users
        where
            username = :username
        ''')

        res = connection.execute(sql, {
            'username':username
            })  
    if res.scalar() == 1:
        return True
    else:
        return False

@app.route("/", methods=['GET', 'POST'])
def root():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    gc = are_credentials_good(username, password)
    # Fix button
    count = request.args.get('page', 0)
    with connection.begin() as trans:
            sql=sqlalchemy.sql.text('''
            SELECT username, created_at, message_text
            FROM tweets
            JOIN users USING (id_users)
            ORDER BY created_at DESC
            LIMIT 20
            OFFSET 20 * :page_count
            ''')

            res = connection.execute(sql,{
                'page_count': count
                })
            tweets = res.fetchall()
    return render_template('root.html', logged_in=gc, tweets=tweets, page=count)

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    gc = are_credentials_good(username, password)
    firstLogin = ((username==None and password==None) or (username=='' and password==''))
    print("gc:", gc, "fl", firstLogin)
    if not gc and firstLogin:
        print("here")
        return render_template('login.html', logged_in=False, bad_credentials=False)
    elif gc and not firstLogin:
        #template = render_template('login.html', logged_in=True, bad_credentials=False)
        print("hello")
        response = make_response(redirect('/'))
        response.set_cookie('username', username)
        response.set_cookie('password', password)
        return response
    else:
        print("hi")
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
    usernameExists = username_exists(username)
    noneCheck = username == None and password1 == None
    passDiff = (password1 != password2)
    gc = are_credentials_good(username, password1)

    print("NC:", noneCheck, "pd:", passDiff, "gc:", gc)

    if noneCheck:
        return render_template('create_account.html')
    elif passDiff: 
        return render_template('create_account.html', diff_password=True)
    elif gc: 
        return render_template('create_account.html', diff_password=False, account_exists=True)
    elif usernameExists:
        return render_template('create_account.html', diff_password=False, account_exists=False, userName_exists=True) 
    else:
        with connection.begin() as trans:
            sql=sqlalchemy.sql.text('''
            INSERT INTO users (
            username,
            password
            ) VALUES (
            :username,
            :password
            )''')

            res = connection.execute(sql, {
                    'username': username,
                    'password': password1
                })
        response = make_response(redirect('/'))
        response.set_cookie('username', username)
        response.set_cookie('password', password1)
        return response
        # return render_template('create_account.html', diff_password=False, account_exists=False)

@app.route("/create_message", methods=['GET', 'POST'])
def create_message():
    # Style HTML more for bigger text so that there is autoscroll
    # Check if the cookies are correct
    message = request.form.get('message')
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    gc = are_credentials_good(username, password)
    if not gc:
         return make_response(redirect('/'))
    notNull = (message != None)
    if gc and notNull:
        with connection.begin() as trans:
            sql=sqlalchemy.sql.text('''
            SELECT id_users
            FROM users
            where
                username = :username AND
                password = :password
            ''')

            res = connection.execute(sql, {
                'username':username,
                'password':password
                })
            userID = res.first()[0]

            sql = sqlalchemy.sql.text('''
            INSERT into tweets (
            id_users,
            message_text,
            created_at
            ) VALUES (
            :id_users,
            :message_text,
            NOW()
            )''')

            res = connection.execute(sql, {
                'id_users': userID,
                'message_text': message
                })

    return render_template('create_message.html', logged_in=True)

@app.route("/search", methods=['GET', 'POST'])
def search():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    gc = are_credentials_good(username, password)
    # Make Search Field Bigger
    search = request.args.get('search')
    count = request.args.get('page', 0)
    with connection.begin() as trans:
            sql=sqlalchemy.sql.text('''
            SELECT 
                username, 
                created_at, 
                TS_HEADLINE(message_text, q,
                    'StartSel="<font color=red><b>",
                    StopSel="</font></b>",
                    MaxFragments=10,
                    MinWords=5, MaxWords=10')
            FROM tweets
            JOIN users USING (id_users)
            CROSS JOIN PLAINTO_TSQUERY(:search) AS q
            WHERE 
                to_tsvector('english', message_text) @@ q
            ORDER BY 
                TS_RANK(to_tsvector('english', message_text), q) DESC,
                created_at DESC
            LIMIT 20
            OFFSET 20 * :page_count
            ''')

            res = connection.execute(sql,{
                'search': search,
                'page_count': count
                })
            tweets = res.fetchall()
    return render_template('search.html', logged_in=gc, tweets=tweets, page=count, search=search)

#@app.route("/static/<path:filename>")
#def staticfiles(filename):
#    return send_from_directory(app.config["STATIC_FOLDER"], filename)
#
#
#@app.route("/media/<path:filename>")
#def mediafiles(filename):
#    return send_from_directory(app.config["MEDIA_FOLDER"], filename)
#
#
#@app.route("/upload", methods=["GET", "POST"])
#def upload_file():
#    if request.method == "POST":
#        file = request.files["file"]
#        filename = secure_filename(file.filename)
#        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
#    return """
#    <!doctype html>
#    <title>upload new File</title>
#    <form action="" method=post enctype=multipart/form-data>
#      <p><input type=file name=file><input type=submit value=Upload>
#    </form>
#    """
