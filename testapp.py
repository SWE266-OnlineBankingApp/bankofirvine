import sqlite3
from datetime import date

conn = sqlite3.connect('bankdata.db')
cur = conn.cursor()
# hi there
username = "testuser"
password='012345'
cur.execute("select * from Login where username = :username", {"username":username})
loginResult = cur.fetchall()
print(loginResult)
if (len(loginResult)==1):
    if (loginResult[0][2] == password):
        print("**** Logging In user****")
        print("username: ", username)
    else:
        print(" Incorrect username or password")
elif (len(loginResult)>1):
    print(" Error multiple users with this username. Check dB")
    exit()
else:
    print(" Incorrect username or password")
    exit()

userId = loginResult[0][0]

#cur.execute("select * from Users")
cur.execute("select * from Users where loginId = :id", {"id": userId})
userResult = cur.fetchall()
print(userResult)
#Fetch checking and savings account balance
checkingAccountNo = userResult[0][6]
savingsAccountNo = userResult[0][5]
cur.execute("select * from Checking_accounts where checkingAccountNo= :checkingAccountNo", {"checkingAccountNo": checkingAccountNo})
checkingResult = cur.fetchall()
print(" ****** checking account details for user*****")
print(checkingResult)
cur.execute("select * from Savings_accounts where savingsAccountNo= :savingsAccountNo", {"savingsAccountNo": savingsAccountNo})
savingsResult = cur.fetchall()
print(" ****** savings account details for user*****")
print(savingsResult)
conn.commit()
cur.close()
