from psycopg2.extensions import connection

from quast.models.User import User

class Question:
    """
    Class representing a Question.
    """

    def __init__(self,
                 author: User=None,
                 title: str=None,
                 body: str=None,
                 upvotes: int=0,
                 downvotes: int=0):
        self._author = author
        self._title = title
        self._body = body
        self._upvotes = upvotes if upvotes else 0
        self._downvotes = downvotes if downvotes else 0

    @staticmethod
    def from_qid(qid: int,
                 conn: connection):
        with conn.cursor() as curs:
            curs.execute("SELECT author, title, description, upvotes, downvotes "
                         "FROM questions "
                         "WHERE qid=%s", (qid, ))
            author, title, body, upvotes, downvotes = curs.fetchone()
        return Question(author=author, title=title, body=body, upvotes=upvotes,
                        downvotes=downvotes)
