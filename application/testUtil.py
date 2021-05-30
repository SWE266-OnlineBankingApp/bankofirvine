from functions.util import validate_num,validate_str,validate_comments
import unittest  

class Test_Util(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_num(self):
        print("Test: validate_num()")
        self.assertTrue(validate_num("0.00"))
        self.assertTrue(validate_num("909.00"))
        self.assertFalse(validate_num("09.000"))
        self.assertTrue(validate_num("9723.37"))


    def test_validate_str(self):
        print("Test: validate_str()")
        self.assertTrue(validate_str("shawn"))
        self.assertTrue(validate_str("..shawn"))
        self.assertFalse(validate_str(".%shawn"))

    def test_validate_comments(self):
        print("Test: validate_comments()")
        self.assertTrue(validate_comments("I love this bank, because of its service."))
        self.assertTrue(validate_comments("   I made a comment."))
        # not end with a period.
        self.assertFalse(validate_comments("aaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbcccccccccc"))
        # some malicious string.
        self.assertFalse(validate_comments("<script>alert('hacked!!')</script>"))


if __name__ == '__main__':
    unittest.main()