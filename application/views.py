import sqlite3
from application import app
from flask import render_template, request, redirect, url_for, session
from application.functions.util import create_salt, hash_password, validate_str, create_random_userid, comments
from application.functions.data_access import create_user, create_account, get_name_from_userid

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
            nfeedback = f"Username or Password is invalid"
            return render_template('home.html',feedback=nfeedback)

        #code to check against DB 
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()
        result = cur.execute("select userId, password, salt from Users where username= ?", (username,)).fetchone()
        conn.close()
        if (not result):
            # invalid username
            app.logger.error("On Login: details not found for username = {}".format(username))
            nfeedback = f"Username or Password is invalid"
            return render_template('home.html',nfeedback=nfeedback)
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
                app.logger.error("On Login: password invalid for username = {}".format(username))
                nfeedback = f"Username or Password is invalid"
                return render_template('home.html',nfeedback=nfeedback)
    
    session.pop("USER",None)                                    
    return render_template('home.html')

@app.route('/about', methods=["GET","POST"])
def about():
    if session.get("USER", None) is not None:
        app.logger.debug("About")

        if(request.method=="POST"):
            comment = request.form.get("comment")
            name = get_name_from_userid(session.get("USER"))
            comments[name[0]]=comment
        return render_template('about.html', comments = comments)

    return redirect(url_for('home'))    

@app.route('/logout')
def logout():
    app.logger.debug("Logging out")
    session.pop("USER",None)
    return redirect(url_for('home'))

@app.route('/register', methods=["GET","POST"])
def register():
    if (request.method== "POST"):
        app.logger.debug("New Registration started")
        username = request.form.get("username")
        password = request.form.get("password")
        initial_balance = request.form.get("ibalance", type= float)
        name = request.form.get("name")
        
        userid = create_random_userid()
        salt = create_salt()
        password_hash = hash_password(password, salt)
        try:
            create_user(userid, username, password_hash, salt, name)
            app.logger.debug("Created new user")
        except sqlite3.IntegrityError as e:
            # uniqu constraint failed. send user back to login page with user already exists
            nfeedback = "User already exists."
            return render_template('home.html',nfeedback=nfeedback)
        else:
            # # user created. get userid for account creation
            # userid = get_userid_from_username(username)
            # app.logger.debug("created userid = {}".format(userid))
            # userid should always be present since we just successfully created a user. nonetheless let's check if a userid was returned by the DB
            # if (userid):
            create_account(initial_balance, userid)
            app.logger.debug("New Registration completed")
            pfeedback = f"Successful registration. Please login"
            return render_template('home.html',pfeedback=pfeedback)
            # else:
            #     app.logger.error("Couldn't locate userid of username= {}".format(username))
            #     feedback = f"Couldn't register. Please contact the administrator"
            #     return render_template('home.html',feedback=feedback)
    else:
        return render_template('register.html') 

@app.route('/account')
def account():
    if session.get("USER", None) is not None:
        userid = session.get("USER")

        app.logger.debug("Account access")
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()
        name = cur.execute("select name from Users where userId= ? ",[userid]).fetchone()
        balance = cur.execute("select currentBalance from Accounts where userid=? ",[userid]).fetchone()
        conn.close()

        if(name == None or balance == None):
            app.logger.error("Account query had empty result")
            nfeedback = f"Something went wrong please login again"
            session.pop("USER",None)
            return render_template('home.html',nfeedback = nfeedback)
        
        return render_template('account.html', name = name[0], balance = balance[0])
    else:
        app.logger.error("Session not set when accessing account")
        return redirect(url_for('home'))   
