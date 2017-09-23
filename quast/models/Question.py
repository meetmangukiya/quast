from psycopg2.extensions import connection
from psycopg2.pool import ThreadedConnectionPool

from quast.models.Answer import Answer
from quast.models.User import User

class Question:
    """
    Class representing a Question.
    """

    def __init__(self,
                 author: str=None,
                 title: str=None,
                 body: str=None,
                 upvotes: int=0,
                 downvotes: int=0,
                 pool: ThreadedConnectionPool=None):
        self._author = author
        self._title = title
        self._body = body
        self._upvotes = upvotes if upvotes else 0
        self._downvotes = downvotes if downvotes else 0
        self._pool = pool

    @staticmethod
    def from_qid(qid: int,
                 pool: ThreadedConnectionPool):
        conn = pool.getconn()
        with conn.cursor() as curs:
            curs.execute("SELECT author, title, description, upvotes, downvotes "
                         "FROM questions "
                         "WHERE qid=%s", (qid, ))
            author, title, body, upvotes, downvotes = curs.fetchone()
        pool.putconn(conn)
        return Question(author=author, title=title, body=body, upvotes=upvotes,
                        downvotes=downvotes, pool=pool)

    def answers(self):
        """
        Return a list of ``quast.models.Answer`` object.
        """
        conn = self._pool.getconn()
        answers = []
        with conn.cursor() as curs:
            curs.execute("SELECT author, body, upvotes, downvotes FROM answers "
                         "WHERE qid=%s", (qid, ))
            for author, body, upvotes, downvotes in curs.fetchone():
                answers.append(Answer(author=author, body=body, upvotes=upvotes,
                                      downvotes=downvotes, qid=qid,
                                      pool=self._pool))
        self._pool.putconn(conn)
        return answers

    def as_dict(self):
        return {
            'author': self._author,
            'title': self._title,
            'description': self._body,
            'upvotes': self._upvotes,
            'downvotes': self._downvotes
        }
