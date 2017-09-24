import hashlib
import os
import uuid

from flask import Flask
from flask import jsonify
from flask import request, session
from flask_session import Session
import psycopg2
from psycopg2.pool import ThreadedConnectionPool

from quast.authentication import login_required, authenticate
from quast.models.Answer import Answer
from quast.models.Question import Question
from quast.models.User import User
from quast.models.Tag import Tag

POOL = ThreadedConnectionPool(
        3, 4, "dbname={} user={}".format(os.environ.get("DB_NAME"),
                                         os.environ.get("DB_USER"))
    )

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "quast-on-quest")
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

# GET Requests
# ============

@app.route("/question/<int:qid>", methods=['GET'])
def question_info(qid):
    """
    Return all question information.
    """
    question = Question.from_qid(qid, POOL)
    answers = question.answers()
    data = question.as_dict()
    data['answers'] = list(map(lambda x: x.as_dict(), answers))
    return jsonify(data)

@app.route("/question/<int:qid>/answer/<answerer>", methods=['GET'])
def answer_info(qid, answerer):
    """
    Return all answer information.
    """
    answer = Answer.from_qid_author(qid, answerer, POOL)
    return jsonify(answer.as_dict())

@app.route("/users/<username>/followers", methods=['GET'])
def user_followers(username):
    """
    Return list of followers of user ``username``.
    """
    user = User.from_username(username, POOL)
    return jsonify(user.get_followers())

@app.route("/user/<username>/questions", methods=['GET'])
def user_questions(username):
    """
    Return list of questions asked by user ``username``.
    """
    user = User.from_username(username, POOL)
    return jsonify(list(map(lambda x: x.as_dict(), user.get_questions())))

@app.route("/tag/<name>/questions", methods=['GET'])
def tags_questions(name):
    """
    Return list of questions tagged ``name``.
    """
    tag = Tag.from_name(name, pool=POOL)
    questions = tag.questions()
    data = tag.as_dict()
    data['questions'] = list(map(lambda x: x.as_dict(), questions))
    return jsonify(data)

# ACCOUNT & SESSION MANAGEMENT
# ============================

@app.route("/login", methods=["POST"])
def login():
    """
    Login the user.
    """
    if authenticate(request.json.get('username'), request.json.get('password'), POOL):
        session["logged_in"] = True
        session["username"] = request.json.get('username')
        return jsonify({"status": "success"})
    return jsonify({"status": "failed"})

@app.route("/logout", methods=["POST"])
def logout():
    """
    Logs out the user.
    """
    session['logged_in'] = False
    return jsonify({"status": "success"})

@app.route("/register", methods=["POST"])
def register_new_user():
    """
    Register a new user.
    """
    salt = uuid.uuid4().bytes
    username = request.json.get('username')
    password = request.json.get('password')
    assert username is not None or password is not None

    pwdhash = hashlib.sha1()
    pwdhash.update(password.encode() + salt)
    digest = pwdhash.digest()

    conn = POOL.getconn()
    with conn.cursor() as curs:
        curs.execute("INSERT INTO users(username, password_hash) VALUES(%s, %s)",
                     (username, digest))
        curs.execute("INSERT INTO salts(username, salt) VALUES(%s, %s)",
                     (username, salt))
        conn.commit()
    POOL.putconn(conn)
    return jsonify({"status": "success"})

# POST Requests

@app.route("/question", methods=['POST'])
@login_required
def create_question():
    """
    Create a new question.
    """
    author = session['username']
    title = request.json.get('title')
    body = request.json.get('body')
    tags = request.json.get('tags')
    question = Question.create(author=author, title=title, body=body, tags=tags,
                               pool=POOL)
    return jsonify(question.as_dict())

@app.route("/tag", methods=['POST'])
@login_required
def create_tag():
    """
    Create a tag.
    """
    author = session['username']
    name = request.json.get('name')
    description = request.json.get('description')
    tag = Tag.create(name=name, description=description, pool=POOL)
    return jsonify(tag.as_dict())

if __name__ == '__main__':
    app.run(debug=True)
