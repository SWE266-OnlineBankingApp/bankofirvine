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

## 5. Unit test to the application

We use Selenium to do unit tests under Chrome. If interested, one has to install the Selenium first:
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
For windows user, add the directory containing driver into your PATH. Or, you can use the following command:
```
setx /m path "%path%;<DIR>"
```

We can now test the application.
Change to the relevant directory and execute the test program.
```
cd bankofirvine/application
python3 testApplication.py
```

CAUTION: You have to start the server every time you want to do the test, since the testing involves registering a new account. 