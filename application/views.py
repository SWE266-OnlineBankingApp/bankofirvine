import sqlite3
from application import app
from flask import render_template, request, redirect, url_for, session, flash
from application.functions.util import create_salt, hash_password, validate_str, validate_num, create_random_userid, comments
from application.functions.data_access import create_user, create_account, get_name_from_userid

# account_holder will be a tuple containing name of the user after login 
account_holder = None

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
                global account_holder
                account_holder = get_name_from_userid(userid)  
                app.logger.debug("Home Page: Account holder -> " + account_holder[0])
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
    global account_holder
    account_holder = None
    return redirect(url_for('home'))

@app.route('/register', methods=["GET","POST"])
def register():
    if (request.method== "POST"):
        app.logger.debug("New Registration started")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("cpassword")
        initial_balance_str = request.form.get("ibalance")
        name = request.form.get("name")
        
        #validate user input. If invalid return error message to the user
        if(not validate_str(username)):
            nfeedback = "Username is not valid. Please select another username"
            return render_template('register.html', feedback=nfeedback)
        if (not validate_str(name)):
            nfeedback = "Name is not valid. Please select another name. (JK! you probably made a typo)"
            return render_template('register.html', feedback=nfeedback)
        if (not validate_num(initial_balance_str)):
            nfeedback = "Initial Balance must be a whole number or a number with two decimal digits."
            return render_template('register.html', feedback=nfeedback)          
        if (password != confirm_password):
            nfeedback = "Password fields do not match. Please try again."
            return render_template('register.html', feedback=nfeedback)
        
        initial_balance = float(initial_balance_str)
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
            # app.logger.debug("created userid = {s}".format(userid))
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
        app.logger.debug("Here: " +userid)
        conn = sqlite3.connect('bankdata.db')
        cur = conn.cursor()
        # name = cur.execute("select name from Users where userId= ? ",[userid]).fetchone()
        balance = cur.execute("select currentBalance from Accounts where userid=? ",[userid]).fetchone()
        conn.close()
        global account_holder
        if(account_holder == None or balance == None):
            app.logger.error("Account query had empty result")
            nfeedback = f"Something went wrong please login again"
            session.pop("USER",None)
            return render_template('home.html',nfeedback = nfeedback)
        
        # return render_template('account.html', name = name[0], balance = balance[0])
        return render_template('account.html', name = account_holder[0], balance = balance[0])
    else:
        app.logger.error("Session not set when accessing account")
        return redirect(url_for('home'))   



@app.route('/account/deposit', methods=("POST",))
def deposit():
    if (request.method == "POST"):
        new_deposit = request.form.get("deposit")
        app.logger.debug("We Have A New Deposit -> " + new_deposit)
        if (not validate_num(new_deposit)):
            # warning user the input format is invalid
            flash("Invalid input. Please enter a whole number or a number with two digits")
            app.logger.debug("Invalid input")
            return redirect(url_for('account'))  
        else:
            # update balance in the database account
            app.logger.debug("Accessing db")
            userid = session.get("USER")
            conn = sqlite3.connect('bankdata.db')
            cur = conn.cursor()
            # does name store in the cache anywhere???
            # name = cur.execute("select name from Users where userId= ? ",[userid]).fetchone()
            cur.execute("update Accounts set currentBalance = currentBalance + ? where userId= ? ", [float(new_deposit), userid])
            conn.commit()
            new_balance = cur.execute("select currentBalance from Accounts where userId= ? ",[userid]).fetchone()
            app.logger.debug("Got new balance -> " + str(new_balance[0]))
            conn.close()
            # update balance shown on the page
            flash("Deposit Completed")
            app.logger.debug("Deposit Completed")
            global account_holder
            app.logger.debug("Got name -> " + account_holder[0])
            return render_template('account.html', name = account_holder[0], balance = new_balance[0])

    
@app.route('/account/withdraw', methods=("POST",))
def withdraw():
    if (request.method == "POST"):
        new_withdraw = request.form.get("withdraw")
        app.logger.debug("We Have A New Withdrawal -> " + new_withdraw)
        if (not validate_num(new_withdraw)):
            # warning user the input format is invalid
            flash("Invalid input. Please enter a whole number or a number with two digits")
            return redirect(url_for('account'))  
        else:
            # check if there is enough amount in the database account
            userid = session.get("USER")
            conn = sqlite3.connect('bankdata.db')
            cur = conn.cursor()
            balance = cur.execute("select currentBalance from Accounts where userId= ? ",[userid]).fetchone()
            if (balance[0] >= float(new_withdraw)):
                # update balance in the database account
                # name = cur.execute("select name from Users where userId= ? ",[userid]).fetchone()
                cur.execute("update Accounts set currentBalance = currentBalance - ? where userId= ? ", [float(new_withdraw), userid])
                conn.commit()
                new_balance = cur.execute("select currentBalance from Accounts where userId= ? ",[userid]).fetchone()
                conn.close()
                # update balance shown on the page
                flash("Withdrawal Completed")
                global account_holder
                return render_template('account.html', name = account_holder[0], balance = new_balance[0])
            else:
                flash("Not Enough Balance")
                return redirect(url_for('account'))  