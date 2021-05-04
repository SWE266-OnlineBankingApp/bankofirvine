from util import validate_str, validate_num
import unittest  # use unittest.TestCase

class Test_Util(unittest.TestCase):
    """ Note that you will need to create this setUp() method if you're testing a class
        
        Lets say you're testing a class.
        Simply creates a class object like the example here, and everything will be passed by the keyword 'self'
            
            def setUp(self):
                self.fav_movie = ['God Father','3 Idiots','The Pursuit of Happiness','Star Wars']
                self.moiveL = MovieLibrary(self.fav_movie)
    """

    # Since util.py don't have any classes, so my example doesn't need to do anything with it
    def setUp(self):
        pass

    def test_validate_num(self):
        print("Test: validate_num()")
        self.assertFalse(validate_num("0"))
        self.assertFalse(validate_num("909"))
        self.assertFalse(validate_num("00.000"))
        self.assertTrue(validate_num("9723.37"))


    def test_validate_str(self):
        print("Test: validate_str()")
        self.assertTrue(validate_str("shawn"))
        self.assertTrue(validate_str("..shawn"))
        self.assertFalse(validate_str(".%shawn"))


""" This enable to run our unit test
    Note that the result will be one of these:
        OK -> all tests are passed:)
        FAIL -> not passed:(
        ERROR -> error raised T_T

    And how long it takes to run all tests
"""
if __name__ == '__main__':
    unittest.main()