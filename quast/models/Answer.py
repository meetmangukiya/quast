from psycopg2.extensions import connection
from psycopg2.pool import ThreadedConnectionPool

class Answer:
    """
    Class representing an Answer.
    """

    def __init__(self,
                 author: str,
                 body: str,
                 upvotes: int,
                 downvotes: int,
                 qid: int,
                 pool: ThreadedConnectionPool=None):
        self._author = author
        self._body = body
        self._upvotes = upvotes
        self._downvotes = downvotes
        self._qid = qid
        self._pool = pool

    @staticmethod
    def from_qid_author(qid: int,
                        author: str,
                        pool: ThreadedConnectionPool=None):
        conn = pool.getconn()
        with conn.cursor() as curs:
            curs.execute("SELECT body, upvotes, downvotes, "
                         "FROM answers "
                         "WHERE author=%(username)s AND qid=%(qid)s",
                         {'username': author, 'qid': qid})
            body, upvotes, downvotes = curs.fetchone()
        pool.putconn(conn)
        return Answer(author=author, body=body, upvotes=upvotes,
                      downvotes=downvotes, qid=qid, pool=pool)

    def as_dict(self):
        return {
            'author': self._author,
            'body': self._body,
            'upvotes': self._upvotes,
            'downvotes': self._downvotes,
            'qid': self._qid
        }
