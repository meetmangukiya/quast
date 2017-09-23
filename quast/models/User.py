from psycopg2.extensions import connection
from psycopg2.pool import ThreadedConnectionPool

from quast.models.Question import Question

class User:
    """
    Class representing a User.
    """

    def __init__(self,
                 username: str=None,
                 credits: int=0,
                 bio: str=None,
                 pool: ThreadedConnectionPool=None):
        self._username = username
        self._credits = int(credits)
        self._bio = str(bio) if bio else ''
        self._pool = pool

    @staticmethod
    def from_username(username: str,
                      pool: connection):
        conn = pool.getconn()
        with conn.cursor() as curs:
            curs.execute("SELECT username, credits, bio "
                         "FROM users WHERE username=%s",
                         (str(username), ))
            username, credits, bio = curs.fetchone()
        pool.putconn(conn)
        return User(username=username, credits=credits, bio=bio, pool=pool)

    def get_followers(self):
        """
        Return a list of users that follow the given user.
        """
        conn = self._pool.getconn()
        with conn.cursor() as curs:
            curs.execute("SELECT followed_by FROM followers "
                         "WHERE following_to=%s", (self._username, ))
            followers = list(map(lambda x: x[0], curs.fetchall()))
        self._pool.putconn(conn)
        return followers

    def as_dict(self):
        return {
            'username': self._username,
            'credits': self._credits,
            'bio': self._bio
        }

    def get_questions(self):
        """
        Return a list of ``quast.models.Question`` objects representing
        questions asked by user ``username``.
        """
        conn = self._pool.getconn()
        questions = []
        with conn.cursor() as curs:
            curs.execute("SELECT title, description, upvotes, downvotes, qid "
                         "FROM questions WHERE author=%s", (self._username, ))
            for title, body, upvotes, downvotes, qid in curs.fetchmany():
                questions.append(Question(title=title, body=body,
                                          upvotes=upvotes, downvotes=downvotes,
                                          qid=qid, author=self._username))
        self._pool.putconn(conn)
        return questions
