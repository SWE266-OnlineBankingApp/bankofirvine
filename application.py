import sqlite3
import hashlib
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        #code to check against DB 
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()
        result = cur.execute('select password, salt from Users where username=?', username)
        if result.rowcount == 0:
            # invalid username
            feedback = f"Username or Password is invalid"
            return render_template('home.html',feedback=feedback)
        else:
            #valid username. check password hash is correct here
            # if password hash correct, return account page
            resultList = result.fetchall()
            stored_password_hash = resultList[0][0]
            stored_salt = resultList[0][1]
            client_password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt, 100000)
            if (client_password_hash == stored_password_hash):
                # password success         
                #return redirect('account')
                pass
            else:
                # password fail
                feedback = f"Username or Password is invalid"
                return render_template('home.html',feedback=feedback)
            

    #return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')    

@app.route('/account')
def account():
    return render_template('account.html')   

def create_db():
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Accounts")
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("CREATE TABLE IF NOT EXISTS Users(userId INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(accountId INTEGER PRIMARY KEY AUTOINCREMENT, currentBalance REAL, userId INTEGER, FOREIGN KEY(userId) REFERENCES Users(userId))")
    #insert a new user with auto-assigned userId=1
    cur.execute('INSERT INTO Users(username, password, name) VALUES(?, ?, ?)', ( 'testuser', '012345', 'testname'))
    # insert an account for user with accountId = 1 auto-assigned and userId=1
    cur.execute('INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)', (5000, 1))

    conn.commit()
    cur.close()

# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
