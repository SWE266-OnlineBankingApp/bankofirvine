from functions.util import validate_num,validate_str,validate_comments, validate_million, validate_trillion
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
        # not end with some illegal character.
        # fix this part later.
#         self.assertFalse(validate_comments("aaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbccccccccccaaaaaaaaaabbbbbbbbbbcccccccccc>"))
        # some malicious string.
        self.assertFalse(validate_comments("<script>alert('hacked!!')</script>"))

    def test_validate_million(self):
        print("Test: validate_comments()")
        self.assertTrue(validate_million(1.00))
        self.assertTrue(validate_million(100000.00))
        # exactly 1 million
        self.assertFalse(validate_million(1000000.00))
        # number larger than 1 million
        self.assertFalse(validate_million(1000000000000.00))

    def test_validate_trillion(self):
        print("Test: validate_comments()")
        self.assertTrue(validate_trillion(100.00))
        self.assertTrue(validate_trillion(1000000.00))
        # exactly 1 trillion
        self.assertFalse(validate_trillion(1000000000000.00))
        # some number larger than 1 trillion
        self.assertFalse(validate_trillion(1000000000000000.00))


if __name__ == '__main__':
    unittest.main()