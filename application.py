import sqlite3
import hashlib
import os
from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    app.logger.debug("Home page accessed")
    if request.method == "POST":
        app.logger.debug("Home page accessed with POST")
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        #code to check against DB 
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()
        result = cur.execute("select userId, password, salt from Users where username= ?", (username,)).fetchone()
        conn.close()
        if (not result):
            # invalid username
            feedback = f"Username or Password is invalid"
            return render_template('home.html',feedback=feedback)
        else:
            #valid username. check password hash is correct here
            # if password hash correct, return account page
            userid = result[0]
            stored_password_hash = result[1]
            stored_salt = result[2]
            client_password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt, 100000)
            if (client_password_hash == stored_password_hash):
                # password success         
                return redirect(url_for('account',userid=userid))
            else:
                # password fail
                # We should not store user's bare password in the logs. Can store only username if wanted
                app.logger.error("On Login details not found for username = {}, password= {}".format(username, password))
                feedback = f"Username or Password is invalid"
                return render_template('home.html',feedback=feedback)
                     
        # validate entered username and password strings 

        #code to check against DB
        #conn = sqlite3.connect('bankdata.db')
        #cur = conn.cursor()   
        #userid = cur.execute("select userId from Users where username= ? and password = ? ",(username, password)).fetchone()  
        #conn.close()
   
        # if(not userid):
        #     app.logger.error("On Login details not found for username = {}, password= {}".format(username, password))
        #     feedback = f"Username or Password is invalid"
        #     return render_template('home.html',feedback=feedback)
        # else:        
        #     return redirect(url_for('account',userid=userid[0]))
                   
    return render_template('home.html')

@app.route('/register')
def register():
    app.logger.debug("New Registration")
    return render_template('register.html')    

@app.route('/account/<userid>')
def account(userid):
    #userid will be encoded needs to be decoded first
    app.logger.debug("Account access by {}".format(userid))
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()    
    name = cur.execute("select name from Users where userid= ? ",[userid]).fetchone()
    balance = cur.execute("select currentBalance from Accounts where userid=? ",[userid]).fetchone()
    conn.close()

    if(name == None or balance == None):
        app.logger.error("Account query had empty result for {}".format(userid))
        feedback = f"Something went wrong please login again"
        return render_template('home.html',feedback = feedback)
    
    return render_template('account.html', name = name[0], balance = balance[0])   


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
    salt1 = os.urandom(32)
    password1 = '012345'
    password_hash = hashlib.pbkdf2_hmac('sha256', password1.encode('utf-8'), salt1, 100000)
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
    

    
