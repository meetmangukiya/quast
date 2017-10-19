import logging

from psycopg2.pool import ThreadedConnectionPool


logger = logging.getLogger()


class Answer:
    """
    Class representing an Answer.
    """

    def __init__(self,
                 author: str,
                 body: str,
                 qid: int,
                 upvotes: int = None,
                 downvotes: int = None,
                 pool: ThreadedConnectionPool = None) -> (None):
        self._author = author
        self._body = body
        self._upvotes = int(upvotes) if upvotes else 0
        self._downvotes = int(downvotes) if downvotes else 0
        self._qid = qid
        self._pool = pool

    @staticmethod
    def from_qid_author(qid: int,
                        author: str,
                        pool: ThreadedConnectionPool = None):
        """
        Retrieve data from database and construct ``Answer`` using it.
        """
        conn = pool.getconn()
        with conn.cursor() as curs:
            curs.execute("SELECT body, upvotes, downvotes "
                         "FROM answers "
                         "WHERE author=%(username)s AND qid=%(qid)s",
                         {'username': author, 'qid': qid})
            body, upvotes, downvotes = curs.fetchone()
        pool.putconn(conn)
        return Answer(author=author, body=body, upvotes=upvotes,
                      downvotes=downvotes, qid=qid, pool=pool)

    def as_dict(self):
        """
        Return all relevant information in form of dict.
        """
        return {
            'author': self._author,
            'body': self._body,
            'upvotes': self._upvotes,
            'downvotes': self._downvotes,
            'qid': self._qid
        }

    def __repr__(self):
        return '<Answer (qid={}, author={})>'.format(self._qid, self._author)

    def __eq__(self, other):
        return (
            self._body == other._body and
            self._author == other._author and
            self._qid == other._qid and
            self._upvotes == other._upvotes and
            self._downvotes == other._downvotes
        )

    def delete(self):
        """
        Delete question ``qid``'s answer whose author is ``author``.
        :returns: ``True`` if successful else ``False``.
        """
        conn = self._pool.getconn()

        try:
            with conn.cursor() as curs:
                curs.execute("DELETE FROM answers WHERE qid=%(qid)s AND "
                             "author=%(author)s ",
                             {'qid': self._qid, 'author': self._author})
            conn.commit()
            return True
        except:  # pragma: no cover, for logging
            logger.exception("An exception occured while deleting answer "
                             " {}".format(self))
            return False
        finally:
            self._pool.putconn(conn)

    @staticmethod
    def create(qid, author, pool, body):
        conn = pool.getconn()
        with conn.cursor() as curs:
            curs.execute("INSERT INTO answers(qid, author, body) "
                         "VALUES(%s, %s, %s)", (qid, author, body))
            conn.commit()
        pool.putconn(conn)
        return Answer(qid=qid, author=author, pool=pool, body=body)
