import sqlite3
from application import app
from flask import render_template, request, redirect, url_for, session, flash
from application.functions.util import create_salt, hash_password, validate_str, validate_num, create_random_userid, comments, validate_comments, validate_largenum
from application.functions.data_access import create_user, create_account, get_user_authentication_info, get_name_from_userid, deposit_and_update, get_currentBalance_from_userid, withdraw_and_update

account_holder = None

@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def error_handler(e):
    app.logger.error("Error Handler "+str(e))
    session.pop("USER",None)
    global account_holder
    account_holder = None
    return render_template('error.html')

@app.route('/', methods=["GET","POST"])
def home():
    try:
        app.logger.debug("Home page accessed")
        if request.method == "POST":
            app.logger.debug("Home page accessed with POST")
            
            username = request.form.get("username")
            password = request.form.get("password")

            #validate the username
            if(not validate_str(username)):
                app.logger.error("username = {} failed validation".format(str(username)))
                nfeedback = f"Username or Password is invalid"
                return render_template('home.html',nfeedback=nfeedback)

            #code to check against DB 
            result = get_user_authentication_info(username)
            if (not result):
                # invalid username
                app.logger.error("On Login: details not found for username = {}".format(str(username)))
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
                    session.permanent = True
                    global account_holder
                    account_holder = get_name_from_userid(userid)  
                    app.logger.debug("Home Page: Account holder -> " + account_holder[0])
                    return redirect(url_for('account'))
                else:
                    # password fail
                    app.logger.error("On Login: password invalid for username = {}".format(str(username)))
                    nfeedback = f"Username or Password is invalid"
                    return render_template('home.html',nfeedback=nfeedback)
        
        session.pop("USER",None)                                    
        return render_template('home.html')
    except Exception as e:
        error_handler(e)        


@app.route('/about', methods=["GET","POST"])
def about():
    try:
        if session.get("USER", None) is not None:
            app.logger.debug("About")
            if(request.method=="POST"):
                comment = request.form.get("comment")
                name = get_name_from_userid(session.get("USER"))
                if (not validate_comments(comment)):
                    # warning user the input format is invalid
                    app.logger.error("Invalid input for comment "+comment)
#                     feedback = f"Invalid input. Please enter a sentence consist of letters, numbers, spaces, and periods."
#                     return render_template("about.html", feedback = feedback)
                else:
                    # update comments
                    app.logger.debug("Preparing comment")
                    comments[name[0]]=comment
                    # notify user deposit completed
                    app.logger.debug("New comment updated")
#                     feedback = f"Comment updated"
#                     return render_template("about.html", feedback = feedback)

            return render_template('about.html', comments = comments)
        else:
            app.logger.error("Session not set when accessing about page")
            error_handler("Session invalid on about")

        return redirect(url_for('home'))   
    except Exception as e:
        error_handler(e)        


@app.route('/logout')
def logout():
    app.logger.debug("Logging out")
    session.pop("USER",None)
    global account_holder
    account_holder = None
    return redirect(url_for('home'))


@app.route('/register', methods=["GET","POST"])
def register():
    try:
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
                app.logger.error("On Register username invalid "+str(username))
                return render_template('register.html', feedback=nfeedback)
            if (not validate_str(name)):
                nfeedback = "Name is not valid. Please select another name. (JK! you probably made a typo)"
                app.logger.error("On Register name invalid "+str(name))
                return render_template('register.html', feedback=nfeedback)
            if (not validate_num(initial_balance_str)):
                nfeedback = "Initial Balance must be a number with two decimal digits in the form x.yy Please try again."
                app.logger.error("On Register initial_balance invalid "+str(initial_balance_str))
                return render_template('register.html', feedback=nfeedback)   
            if (not validate_str(password)):
                nfeedback = "Password is not valid. Password may only contain digits 0-9, letters a-z, and special characters _-. only" 
                app.logger.error("On Register password invalid "+str(password))
                return render_template('register.html', feedback=nfeedback)   
            if (password != confirm_password):
                nfeedback = "Password fields do not match. Please try again."
                app.logger.error("On Register password-cpassword mismatch ")
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
                app.logger.error("On Register user exists ")
                nfeedback = "User already exists."
                return render_template('home.html',nfeedback=nfeedback)
            else:
                create_account(initial_balance, userid)
                app.logger.debug("New Registration completed")
                pfeedback = f"Successful registration. Please login"
                return render_template('home.html',pfeedback=pfeedback)
        else:
            return render_template('register.html') 
    except Exception as e:
        error_handler(e)            


@app.route('/account')
def account():
    try:
        if session.get("USER", None) is not None:
            userid = session.get("USER")
            app.logger.debug("Account access")
            balance = get_currentBalance_from_userid(userid)
            global account_holder
            if(account_holder == None or balance == None):
                app.logger.error("Account query had empty result")
                nfeedback = f"Something went wrong please login again"
                session.pop("USER",None)
                return render_template('home.html',nfeedback = nfeedback)
            
            return render_template('account.html', name = account_holder[0], balance = "{:.2f}".format(balance[0]))
        else:
            app.logger.error("Session not set when accessing account")
            return redirect(url_for('home'))  
    except Exception as e:
        error_handler(e)            


@app.route('/account/deposit', methods=("POST",))
def deposit():
    try:
        if session.get("USER", None) is not None:
            if (request.method == "POST"):
                new_deposit = request.form.get("deposit")
                app.logger.debug("We Have A New Deposit -> " + new_deposit)
                if (not validate_num(new_deposit)):
                    # warning user the input format is invalid
                    flash("Invalid input. Please enter a number with two decimal digits in the form x.yy")
                    app.logger.error("Invalid input for deposit "+str(new_deposit))
                    return redirect(url_for('account'))
                elif (not validate_largenum(new_deposit)):
                    # warning user the input format is invalid
                    flash("The input amount is too big. Please enter a number within 1 trillion (or 12 digits for the integral part)")
                    app.logger.error("Input too large for deposit "+str(new_deposit))
                    return redirect(url_for('account'))
                else:
                    # update balance in the database account
                    app.logger.debug("Accessing db")
                    userid = session.get("USER")
                    deposit_and_update(new_deposit, userid)
                    # notify user deposit completed
                    flash("Deposit Completed")
                    app.logger.debug("Deposit Completed")
                    return redirect(url_for('account'))

        else:
            app.logger.error("Session not set when accessing account deposit")
            error_handler("Session invalid on deposit")              
    except Exception as e:
        error_handler(e)
    

@app.route('/account/withdraw', methods=("POST",))
def withdraw():
    try:
        if session.get("USER", None) is not None:
            if (request.method == "POST"):
                new_withdraw = request.form.get("withdraw")
                app.logger.debug("We Have A New Withdrawal -> " + new_withdraw)
                if (not validate_num(new_withdraw)):
                    # warning user the input format is invalid
                    app.logger.error("Invalid input for withdraw "+str(new_withdraw))
                    flash("Invalid input. Please enter a number with upto two decimals in the form x.yy")
                    return redirect(url_for('account'))  
                else:
                    # check if there is enough amount in the database account
                    userid = session.get("USER")
                    balance = get_currentBalance_from_userid(userid)
                    if (balance[0] >= float(new_withdraw)):
                        # update balance
                        withdraw_and_update(new_withdraw, userid)
                        flash("Withdrawal Completed")
                        return redirect(url_for('account'))  
                    else:
                        app.logger.error("Withdrawal attempt with insufficient balance")
                        flash("Not Enough Balance")
                        return redirect(url_for('account'))
        else:
            app.logger.error("Session not set when accessing account withdraw")
            error_handler("Session invalid on withdraw")
            
    except Exception as e:
        error_handler(e)                   