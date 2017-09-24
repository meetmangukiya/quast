from functools import wraps
import hashlib

from flask import session, jsonify, make_response

def authenticate(username, password, POOL):
    conn = POOL.getconn()
    with conn.cursor() as curs:
        curs.execute("SELECT salt FROM salts WHERE username=%s", (username, ))
        (salt, ) = curs.fetchone()
        pwdhash = hashlib.sha1()
        pwdhash.update(password.encode() + salt)
        curs.execute("SELECT password_hash FROM users WHERE username=%s",
                     (username, ))
        (db_hash, ) = curs.fetchone()

    POOL.putconn(conn)
    if bytes(db_hash) == pwdhash.digest():
        return True
    return False

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is True:
            return func(*args, **kwargs)
        else:
            return make_response("whats up")
    return decorated_function
