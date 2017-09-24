import os

from flask import Flask
from flask import jsonify
from flask import request
from psycopg2.pool import ThreadedConnectionPool

from quast.models.Answer import Answer
from quast.models.Question import Question
from quast.models.User import User

POOL = ThreadedConnectionPool(
        3, 4, "dbname={} user={}".format(os.environ.get("DB_NAME"),
                                         os.environ.get("DB_USER"))
    )

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
