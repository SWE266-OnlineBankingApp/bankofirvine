# bankofirvine

## Prerequisites
check your python version: python --version
* [Python3](https://www.python.org/downloads/)

## 1. Clone bankofirvine
```
git clone https://github.com/SWE266-OnlineBankingApp/bankofirvine.git
cd bankofirvine
```

## 2. Set up virtual enviroment and install dependecies 
Set up virtual enviroment at your prefered directory (\<DIR>) and install dependecies within the enviroment
```
python3 -m venv <DIR>
source <DIR>/bin/activate
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

## 4. Instruction of bankofirvine user

After connecting to the website, the user will face the homepage first. Here, the user can create a new account by clicking the Register text on the left, or login with his account. 

After login successfully, the user will be directed to the account page. One can deposit or withdraw on the right, and the information will be shown on the left-hand side. 

## 5. Unit tests

There are two parts of testing in this application.

### Utility testing

The utilities tested here are the validations we used in validating strings and numbers.
For testing them, we use the unittest framework in Python. And one can execute the python file under the application directory.

For executing this test, one can run the file in python

```
cd application
python3 testUtil.py
```

### Application testing

We use Selenium to do unit tests under Chrome browser. We covered 4 categories of testing here, including login, registration, deposit and withdrawal.
The Selenium helps us automatically open the browser, input the test data, check results, and close the browser.

### Executing Selenium testing

If interested, one has to install the Selenium first:
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

After all the preparations, we can now test the application.
Change to the relevant directory and execute the test program.
```
cd bankofirvine/application
python3 testApplication.py
```

CAUTION: You have to start the server every time you want to do the test, since the testing involves registering a new account.