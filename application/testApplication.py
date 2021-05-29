import unittest  # use unittest.TestCase
# for executing unit tests from up to down.
unittest.TestLoader.sortTestMethodsUsing = None
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class Test_Application(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

#         logout() test skipped, since it's tested in home()
#     def testLogout(self):
#         print("Test: logout()")

    def testRegister(self):
        driver = self.driver
        print("\n ----- Registration test begin ----- \n")
        # test registration success
        print("Test: register success")
        driver.find_element_by_id("register").click()
        driver.find_element_by_id("name").send_keys("adam")
        driver.find_element_by_id("uname").send_keys("testuser001")
        driver.find_element_by_id("password").send_keys("1234")
        driver.find_element_by_id("cpassword").send_keys("1234")
        driver.find_element_by_id("ibalance").send_keys("10.00")
        driver.find_element_by_id("register").click()
        assert driver.title == "Home | Bank of Irvine"
        assert ("Successful registration. Please login" in driver.page_source)

        # test registration fail part
        print ("Test: registration fail, repetitive username")
        driver.find_element_by_id("register").click()
        driver.find_element_by_id("name").send_keys("adam")
        driver.find_element_by_id("uname").send_keys("testuser001")
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_id("cpassword").send_keys("12345")
        driver.find_element_by_id("ibalance").send_keys("10.00")
        driver.find_element_by_id("register").click()
        assert driver.title == "Home | Bank of Irvine"
        assert ("User already exists." in driver.page_source)

        print ("Test: registration fail, invalid username")
        driver.find_element_by_id("register").click()
        driver.find_element_by_id("name").send_keys("adam")
        driver.find_element_by_id("uname").send_keys("!testusername")
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_id("cpassword").send_keys("12345")
        driver.find_element_by_id("ibalance").send_keys("10.00")
        driver.find_element_by_id("register").click()
        assert driver.title == "Register | Bank of Irvine"
        assert ("Username is not valid. Please select another username" in driver.page_source)

        print ("Test: registration fail, invalid password")
        driver.find_element_by_id("name").send_keys("adam")
        driver.find_element_by_id("uname").send_keys("testuser123")
        driver.find_element_by_id("password").send_keys("!!!")
        driver.find_element_by_id("cpassword").send_keys("!!!")
        driver.find_element_by_id("ibalance").send_keys("10.00")
        driver.find_element_by_id("register").click()
        assert driver.title == "Register | Bank of Irvine"
        assert ("Password is not valid. Password may only contain digits 0-9, letters a-z, and special characters _-. only" in driver.page_source)

        print ("Test: registration fail, invalid balance")
        driver.find_element_by_id("name").send_keys("adam")
        driver.find_element_by_id("uname").send_keys("testuser123")
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_id("cpassword").send_keys("12345")
        driver.find_element_by_id("ibalance").send_keys("-5.00")
        driver.find_element_by_id("register").click()
        assert driver.title == "Register | Bank of Irvine"

    def testLogin(self):
        driver = self.driver
        print("\n ----- Login test begin ----- \n")
        username = "testuser001"
        password='1234'
        print("Test: login success")
        # test - login success
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("signin").click()
        assert driver.title == "Account | Bank of Irvine"

        # test - login fail, incorrect password.
        print("Test: login fail, incorrect password")
        driver.find_element_by_id("logoutbtn").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys("0123")
        driver.find_element_by_id("signin").click()
        assert driver.title == "Home | Bank of Irvine"
        assert ("Username or Password is invalid" in driver.page_source)

        # test - login fail, nonexist username.
        print("Test: login fail, non-exist username")
        driver.find_element_by_id("username").send_keys("testurrr")
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("signin").click()
        assert driver.title == "Home | Bank of Irvine"
        assert ("Username or Password is invalid" in driver.page_source)


    def testDeposit(self):
        print("\n ----- Deposit test begin ----- \n")
        driver = self.driver
        username = "testuser001"
        password='1234'
        print ("Test: deposit success")
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("signin").click()
        driver.find_element_by_id("Depositinput").send_keys("10.00")
        driver.find_element_by_id("Depositbtn").click()
        assert driver.title == "Account | Bank of Irvine"
        self.assertTrue("Deposit Completed" in driver.page_source)

    def testWithdraw(self):
        print("\n ----- Withdrawal test begin ----- \n")
        driver = self.driver
        username = "testuser001"
        password='1234'
        # test authorized withdraw
        print("Test: withdraw success")
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("signin").click()
        driver.find_element_by_id("Withdrawalinput").send_keys("10.00")
        driver.find_element_by_id("Withdrawalbtn").click()
        assert driver.title == "Account | Bank of Irvine"
        self.assertTrue("Withdrawal Completed" in driver.page_source)
        # test withdraw amount larger
        print("Test: withdraw fail, amount larger than current balance")
        driver.find_element_by_id("Withdrawalinput").send_keys("999999.00")
        driver.find_element_by_id("Withdrawalbtn").click()
        assert driver.title == "Account | Bank of Irvine"
        self.assertTrue("Not Enough Balance" in driver.page_source)

    def tearDown(self):
        self.driver.close()

def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(Test_Application('testRegister'))
    suite.addTest(Test_Application('testLogin'))
    suite.addTest(Test_Application('testDeposit'))
    suite.addTest(Test_Application('testWithdraw'))
    return suite

if __name__ == '__main__':
      runner = unittest.TextTestRunner(failfast=True)
      runner.run(testSuite())