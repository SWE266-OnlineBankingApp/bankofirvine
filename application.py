import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        #code to check against DB 
        #assuming invalid
        feedback = f"Username or Password is invalid"
        return render_template('home.html',feedback=feedback)
       
        # assuming correct
        #return redirect('account')

    return render_template('home.html')

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
    cur.execute("CREATE TABLE IF NOT EXISTS Users(userId INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, email TEXT, name TEXT, address TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(accountId INTEGER PRIMARY KEY AUTOINCREMENT, currentBalance REAL, userId INTEGER, FOREIGN KEY(userId) REFERENCES Users(userId))")
    #insert a new user with auto-assigned userId=1
    cur.execute('INSERT INTO Users(username, password, email, name) VALUES(?, ?, ?, ?)', ( 'testuser', '012345', 'test@gmail.com', 'testname'))
    # insert an account for user with accountId = 1 auto-assigned and userId=1
    cur.execute('INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)', (5000, 1))

    conn.commit()
    cur.close()

# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
