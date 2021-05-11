# bankofirvine

## Prerequisites
check your python version: python --version
* [Python3](https://www.python.org/downloads/)

## 1. Clone bankofirvine
In your preferred directory
```
git clone https://github.com/SWE266-OnlineBankingApp/bankofirvine.git
```

## 2. Set up virtual enviroment and install dependecies 
Set up a virtual enviroment at your preferred directory from previous step and install dependecies within the enviroment
For Mac
```
python3 -m venv ./
source ./bin/activate
cd bankofirvine
python3 -m pip install -r requirements.txt
```

For Windows
```
py -m venv .\
.\Scripts\activate
cd bankofirvine
python3 -m pip install -r requirements.txt
```

## 3. Run the app locally
Run bankofirvine in production enviroment 
For Mac
```
export FLASK_APP=run
flask run
```

For Windows
```
set FLASK_APP=run
flask run
```
View bankofirvine app at: http://localhost:5000

## 4. Instruction for bankofirvine user

After connecting to the url, the user will see the homepage first. Here, the user can create a new account by clicking the Register link on the left, or login with his account. 

After logging in successfully, the user will be directed to the account page. One can deposit or withdraw on the right, and the information will be shown on the left-hand side. 

## 5. Unit tests

This application was tested in two parts.

### Utility testing

The Unittest framework in Python was used to test helper utility methods. 

For executing this test, one can run the file in python

```
cd application
python3 testUtil.py
```

### Application testing

Selenium was used to perform unit tests in the Chrome browser. 

### Executing Selenium testing

If interested, one has to install Selenium first:
```
pip3 install selenium
```

Download a Chrome driver: (version 90. recommended)
```
https://sites.google.com/a/chromium.org/chromedriver/downloads
```

For mac user, put the driver in the following path:
```
/usr/local/bin
```

For macOS version higher than 10.15, remember to approve the usage of driver with this command:
```
xattr -d com.apple.quarantine chromedriver
```
For Windows user, add the directory containing driver into your PATH. Or, you can use the following command:
```
setx /m path "%path%;<DIR>"
```

After all these preparations, we can now test the application.
Change to the relevant directory and execute the test program.
```
cd bankofirvine/application
python3 testApplication.py
```

CAUTION: You have to start the server every time you want to do the test, since testing involves registering a new account.