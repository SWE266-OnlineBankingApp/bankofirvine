import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from application.functions.util import create_salt, hash_password, validate_str

app = Flask(__name__, template_folder='./application/templates')
app.config['SECRET_KEY'] = 'bQ9J84inbtoUcjLZFbQTVg'

@app.route('/', methods=["GET","POST"])
def home():
    app.logger.debug("Home page accessed")
    if request.method == "POST":
        app.logger.debug("Home page accessed with POST")
           
        username = request.form.get("username")
        password = request.form.get("password")

        #validate the username
        if(not validate_str(username)):
            app.logger.error("username = {} failed validation".format(username))
            feedback = f"Username or Password is invalid"
            return render_template('home.html',feedback=feedback)

        #code to check against DB 
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()
        result = cur.execute("select userId, password, salt from Users where username= ?", (username,)).fetchone()
        conn.close()
        if (not result):
            # invalid username
            app.logger.error("On Login: details not found for username = {}".format(username))
            feedback = f"Username or Password is invalid"
            return render_template('home.html',feedback=feedback)
        else:
            #valid username. check password hash is correct here
            # if password hash correct, return account page
            userid = result[0]
            stored_password_hash = result[1]
            stored_salt = result[2]
            client_password_hash = hash_password(password, stored_salt)
            if (client_password_hash == stored_password_hash):
                # password success
                session["USER"] = userid       
                return redirect(url_for('account'))
            else:
                # password fail
                app.logger.error("On Login: hash details invalid for username = {}".format(username))
                feedback = f"Username or Password is invalid"
                return render_template('home.html',feedback=feedback)
                                        
    return render_template('home.html')

@app.route('/logout')
def logout():
    app.logger.debug("Logging out")
    session.pop("USER",None)
    return redirect(url_for('home'))

@app.route('/register', methods=["GET","POST"])
def register():
    if (request.method== "POST"):
        app.logger.debug("New Registration started")
        username = request.form.get("uname")
        password = request.form.get("pass")
        initial_balance = request.form.get("ibalance", type= float)
        name = request.form.get("name")
        salt = create_salt()
        password_hash = hash_password(password, salt)
        try:
            create_user(username, password_hash, salt, name)
        except sqlite3.IntegrityError as e:
            # uniqu constraint failed. send user back to login page with user already exists
            feedback = "User already exists."
            return render_template('home.html',feedback=feedback)
        else:
            # user created. get userid for account creation
            userid = get_userid_from_username(username)
            app.logger.debug("username={}, password_hash={}, initial_balance={}, name={}".format(username, password_hash, initial_balance, name))
            app.logger.debug("created userid = {}".format(userid))
            # userid should always be present since we just successfully created a user. nonetheless let's check if a userid was returned by the DB
            if (userid):
                create_account(initial_balance, userid)
                app.logger.debug("New Registration completed")
                feedback = f"Successful registration."
                return render_template('home.html',feedback=feedback)
            else:
                app.logger.error("Couldn't locate userid of username= {}".format(username))
                feedback = f"Couldn't register user. Please contact the administrator"
                return render_template('home.html',feedback=feedback)
    else:
        return render_template('register.html') 

@app.route('/account')
def account():
    if session.get("USER", None) is not None:
        userid = session.get("USER")

        app.logger.debug("Account access by {}".format(userid))
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()    
        name = cur.execute("select name from Users where userId= ? ",[userid]).fetchone()
        balance = cur.execute("select currentBalance from Accounts where userid=? ",[userid]).fetchone()
        conn.close()

        if(name == None or balance == None):
            app.logger.error("Account query had empty result for {}".format(userid))
            feedback = f"Something went wrong please login again"
            return render_template('home.html',feedback = feedback)
        
        return render_template('account.html', name = name[0], balance = balance[0])
    else:
        app.logger.error("Session not set when accessing account")
        return redirect(url_for('home'))   

def create_user(username, password_hash, salt, name):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Users(username, password, salt, name) VALUES(?, ?, ?, ?)", (username, password_hash, salt, name))
    except sqlite3.IntegrityError as e:
        raise sqlite3.IntegrityError
    finally:
        conn.commit()
        cur.close()

def get_userid_from_username(username):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    userid = cur.execute("SELECT userid from Users where username = ?", (username,)).fetchone()[0]
    conn.commit()
    cur.close()
    return userid


def create_account(initial_balance, userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)", (initial_balance, userid))
    conn.commit()
    cur.close()

def create_db():
    app.logger.debug("Initiate DB creation")
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Accounts")
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("CREATE TABLE IF NOT EXISTS Users(userId INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, salt TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(accountId INTEGER PRIMARY KEY AUTOINCREMENT, currentBalance REAL, userId INTEGER, FOREIGN KEY(userId) REFERENCES Users(userId))")
    #insert a new user with auto-assigned userId=1
    password1 = '012345'
    salt1 = create_salt()
    password_hash = hash_password(password1,salt1)
    cur.execute('INSERT INTO Users(username, password, salt, name) VALUES(?, ?, ?, ?)', ( 'testuser', password_hash, salt1, 'testname'))
    # insert an account for user with accountId = 1 auto-assigned and userId=1
    cur.execute('INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)', (5000, 1))

    conn.commit()
    cur.close()
    app.logger.debug("DB Created")

# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
