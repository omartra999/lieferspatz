from functools import wraps
from flask import session, redirect, url_for

#Decorator function to check if a user is logged in
def login_required_customer(function):
    @wraps(function)
    def decorated_function(*args,**kwargs):
        if "logged_in" not in session:
            return redirect(url_for('login'))
        return function(*args, **kwargs)
    return decorated_function

def login_required_restaurant(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "logged_in_restaurant" not in session:
            return redirect(url_for('restaurant_login'))
        return function(*args, **kwargs)
    return decorated_function