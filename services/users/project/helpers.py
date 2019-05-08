import re

def validate_email(val):
   return  re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", val) != None

def validate_password(val):
   return len(val) >=6 and re.search('[0-9]',val) is not None and re.search('[a-z]', val) is not None
