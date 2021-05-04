import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
         
        # validate entered username and password strings 

        #code to check against DB
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()   
        userid = cur.execute("select userId from Users where username= ? and password = ? ",(username, password)).fetchone()  
        conn.close()
   
        if(not userid):
            feedback = f"Username or Password is invalid"
            return render_template('home.html',feedback=feedback)
        else:        
            return redirect(url_for('account',userid=userid[0]))
                   
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')    

@app.route('/account/<userid>')
def account(userid):
    #userid will be encoded needs to be decoded first

    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()    
    name = cur.execute("select name from Users where userid= ? ",[userid]).fetchone()
    balance = cur.execute("select currentBalance from Accounts where userid=? ",[userid]).fetchone()
    conn.close()

    if(name == None or balance == None):
        feedback = f"Something went wrong please login again"
        return render_template('home.html',feedback = feedback)
    
    return render_template('account.html', name = name[0], balance = balance[0])   


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
    

    
