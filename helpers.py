import re


def checkUser(email):
    """ check user login username or email, phone """
    if '@' in email:
        kwargs = {'email': email}
    elif email.isdigit() == True:
        kwargs = {'phone': email}
    else:
        kwargs = {'username': email}
        
    return kwargs
        
# password validation
def password_validate(password):
    msg = ''
    while True:
        if len(password) < 5:
           msg = "Make sure your password is at lest 5 letters"
           return msg
        elif re.search('[0-9]',password) is None:
            msg = "Make sure your password has a number in it"
            return msg
        elif re.search('[A-Z]',password) is None:
            msg = "Make sure your password has a capital letter in it"
            return msg
        else:
            msg = True
            break

    return True

 