from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
import re
def validate_phone_number(phone):
    phone_pattern = r'^(05|06|07)[0-9]{8}$'
    if re.match(phone_pattern, phone):
        return True
    else:
        return False

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(pattern, email):
        return True
    return False
