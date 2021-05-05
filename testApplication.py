# from util import validate_str, validate_num
from application import home, logout, register, account
import unittest  # use unittest.TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# class TestBase(unittest.TestCase):
#     def setUp(self):
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument("headless")
#         chrome_options.add_argument("window-size=1920x1080")
#         self.driver = webdriver.Chrome(options=chrome_options)
#
#     def tearDown(self):
#         self.driver.close()

# class Test_Application(TestBase):
class Test_Application(unittest.TestCase):
    """ Note that you will need to create this setUp() method if you're testing a class

        Lets say you're testing a class.
        Simply creates a class object like the example here, and everything will be passed by the keyword 'self'
            
            def setUp(self):
                self.fav_movie = ['God Father','3 Idiots','The Pursuit of Happiness','Star Wars']
                self.moiveL = MovieLibrary(self.fav_movie)
    """

    # Since util.py don't have any classes, so my example doesn't need to do anything with it
    """
    def test_validate_num(self):
        print("Test: validate_num()")
        self.assertFalse(validate_num("0"))
        self.assertFalse(validate_num("909"))
        self.assertFalse(validate_num("00.000"))
        self.assertTrue(validate_num("9723.37"))

    """

    # quick learning unit tests in Python.
#     def test(self) :
#         print("sample test")
#         self.assertFalse(False)
#         self.assertTrue(True)

#     def setUp(self):
#         super().setUp()
#         self.home = HomePage(self.driver)

    # I prefer this style, it's much clear.
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def testHome(self):
        driver = self.driver
        username = "testuser"
        password='012345'
        print("Test login functions in home()")
#         print(driver.title)
        # test - login success
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("signin").click()
#         self.assertTrue(False)
#         wait = WebDriverWait(driver, 10)
#         print(driver.title)
        assert driver.title == "Account | Bank of Irvine"

        # test - login fail
        driver.find_element_by_id("logoutbtn").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys("0123")
        driver.find_element_by_id("signin").click()
        assert driver.title == "Home | Bank of Irvine"

        # I think that logout() doesn't have to be tested, since it's tested in home()
#     def testLogout(self):
#         print("Test: logout()")

    def testRegister(self):
        driver = self.driver
        print("Test: register()")
        driver.find_element_by_id("register").click()
        assert driver.title == "Register | Bank of Irvine"


#     def testAccount(self):
#         print("Test: account()")

    def tearDown(self):
        self.driver.close()

    # I don't want to get involved in this... DAMN.
#     def testCreateDB(self):
#         print("Test: create_db()")





""" This enable to run our unit test
    Note that the result will be one of these:
        OK -> all tests are passed:)
        FAIL -> not passed:(
        ERROR -> error raised T_T

    And how long it takes to run all tests
"""
if __name__ == '__main__':
    unittest.main()