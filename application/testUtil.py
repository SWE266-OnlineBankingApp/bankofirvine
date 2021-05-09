from functions.util import validate_num,validate_str
import unittest  

class Test_Util(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_num(self):
        print("Test: validate_num()")
        self.assertTrue(validate_num("0"))
        self.assertTrue(validate_num("909"))
        self.assertFalse(validate_num("09.000"))
        self.assertTrue(validate_num("9723.37"))


    def test_validate_str(self):
        print("Test: validate_str()")
        self.assertTrue(validate_str("shawn"))
        self.assertTrue(validate_str("..shawn"))
        self.assertFalse(validate_str(".%shawn"))

if __name__ == '__main__':
    unittest.main()