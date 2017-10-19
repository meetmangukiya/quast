import hashlib
import os
import uuid

from flask import Flask
from flask import jsonify, url_for
from flask import redirect, request, render_template, session, make_response
from flask_session import Session
from psycopg2.pool import ThreadedConnectionPool

from quast.authentication import login_required, authenticate
from quast.models.Answer import Answer
from quast.models.Question import Question
from quast.models.User import User
from quast.models.Tag import Tag
from quast.utils import data_as_dict

POOL = ThreadedConnectionPool(
    3, 4, "dbname={} user={}".format(
        os.environ.get("DB_NAME"),
        os.environ.get("DB_USER")
    )
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "quast-on-quest")
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

# GET Requests
# ============


@app.route("/question/<int:qid>/", methods=['GET'])
def question_info(qid):
    """
    Return all question information.
    """
    question = Question.from_qid(qid, POOL)

    # For serving data as JSON
    #
    # answers = question.answers()
    # data = question.as_dict()
    # data['answers'] = list(map(lambda x: x.as_dict(), answers))
    # return jsonify(data)
    return render_template('question/details.html', question=question)


@app.route("/question/<int:qid>/answer/<answerer>", methods=['GET'])
def answer_info(qid, answerer):
    """
    Return all answer information.
    """
    answer = Answer.from_qid_author(qid, answerer, POOL)
    return jsonify(answer.as_dict())


@app.route("/user/me", methods=['GET'])
def current_user():
    """
    Return information of logged in user.
    """
    if session.get('logged_in'):
        user = User.from_username(session['username'], POOL)
        return jsonify(user.as_dict())
    else:
        return make_response(jsonify({'error': 'Not logged in'}), 401)


@app.route("/user/<username>/followers", methods=['GET'])
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


@app.route("/search/tags", methods=['GET'])
def search_tags():
    """
    Returns list of tags after searching string.
    """
    name = request.args.get('name')
    return jsonify(Tag.search(name, POOL))


# ACCOUNT & SESSION MANAGEMENT
# ============================


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Login the user.
    """
    if request.method == 'POST':
        json = data_as_dict(request)

        if authenticate(json.get('username'), json.get('password'), POOL):
            session["logged_in"] = True
            session["username"] = json.get('username')
            return jsonify({"status": "success"})
        return make_response(jsonify({"status": "failed"}), 401)
    else:
        return render_template('login.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    """
    Logs out the user.
    """
    session['logged_in'] = False
    session.clear()
    return jsonify({"status": "success"})


@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    """
    Register a new user.
    """
    if request.method == 'POST':
        json = data_as_dict(request)
        username = json.get('username')
        password = json.get('password')
        salt = uuid.uuid4().bytes
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
    else:
        return render_template('register.html')

# POST Requests


@app.route("/question/new", methods=['POST', 'GET'])
@login_required
def create_question():
    """
    Create a new question.
    """
    if request.method == 'POST':
        author = session['username']
        json = data_as_dict(request)
        title = json.get('title')
        body = json.get('body')
        tags = list(map(lambda x: x.strip(), json.get('tags').split(',')))
        question = Question.create(author=author, title=title, body=body, tags=tags,
                                   pool=POOL)
        return jsonify(question.as_dict())
    else:
        return render_template('question/new.html')


@app.route("/question/<int:qid>/answer", methods=['POST', 'GET'])
@login_required
def create_answer(qid):
    """
    Adds an answer to a given question.
    """
    if request.method == 'POST':
        author = session['username']
        json = data_as_dict(request)
        body = json.get('body')
        answer = Answer.create(body=body, author=author, qid=qid, pool=POOL)
        return redirect(url_for("/question/{}#answer-{}".format(qid, author)))
    else:
        return render_template('answer/new.html',
                               question=Question.from_qid(qid, POOL))


@app.route("/tag", methods=['POST'])
@login_required
def create_tag():
    """
    Create a tag.
    """
    json = request.get_json()
    name = json.get('name')
    description = json.get('description')
    tag = Tag.create(name=name, description=description, pool=POOL)
    return jsonify(tag.as_dict())


if __name__ == '__main__':
    app.run(debug=True)
