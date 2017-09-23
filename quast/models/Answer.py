from psycopg2.extensions import connection

from quast.models.User import User

class Answer:
    """
    Class representing an Answer.
    """

    def __init__(self,
                 author: User,
                 body: str,
                 upvotes: int,
                 downvotes: int,
                 qid: int):
        self._author = author
        self._body = body
        self._upvotes = upvotes
        self._downvotes = downvotes
        self._qid = qid

    @staticmethod
    def from_qid_author(qid: int,
                        author: User,
                        conn: connection):
        with conn.cursor() as curs:
            curs.execute("SELECT body, upvotes, downvotes, "
                         "FROM answers"
                         "WHERE author=%(username)s AND qid=%(qid)s",
                         {'username': User.username, 'qid': qid})
            body, upvotes, downvotes = curs.fetchone()
        return Answer(author=author, body=body, upvotes=upvotes,
                      downvotes=downvotes, qid=qid)
