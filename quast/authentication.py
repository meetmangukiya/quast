from functools import wraps
import hashlib

from flask import jsonify, make_response, session


def authenticate(username, password, pool):
    """
    Authenticate user with the given username and password.
    """
    conn = pool.getconn()
    with conn.cursor() as curs:
        curs.execute("SELECT salt FROM salts WHERE username=%s", (username, ))
        (salt, ) = curs.fetchone()
        pwdhash = hashlib.sha1()
        pwdhash.update(password.encode() + salt)
        curs.execute("SELECT password_hash FROM users WHERE username=%s",
                     (username, ))
        (db_hash, ) = curs.fetchone()

    pool.putconn(conn)
    if bytes(db_hash) == pwdhash.digest():
        return True
    return False


def login_required(func):
    """
    Returns 401 if the user is not logged in and tries to access restricted
    content.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is True:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({"error": "Unauthorized"}), 401)
    return decorated_function
