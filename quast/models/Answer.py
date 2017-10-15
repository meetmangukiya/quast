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
                 upvotes: int,
                 downvotes: int,
                 qid: int,
                 pool: ThreadedConnectionPool = None) -> (None):
        self._author = author
        self._body = body
        self._upvotes = int(upvotes)
        self._downvotes = int(downvotes)
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

