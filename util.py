""" input validation helper functions of bankofirvine 
"""
import re

# Numeric validation (e.g. balance)
def validate_num (num_input):
    return re.match("((^[1-9][0-9]*)|(^0))(\.[0-9]{2})$", num_input) != None

# String validation (e.g. account name, password)
def validate_str (str_input):
    return re.match("(^[_\\-\\.0-9a-z]{1,127}$)", str_input) != None
    

if __name__ == "__main__":
    print("test1", validate_num ("0"))
    print("test2", validate_num ("909"))
    print("test3", validate_num ("00.000"))
    print("test4", validate_num ("9723.37"))
    print("test5", validate_str ("shawn"))
    print("test6", validate_str ("..shawn"))
    print("test7", validate_str (".%shawn"))