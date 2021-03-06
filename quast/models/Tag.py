from psycopg2.pool import ThreadedConnectionPool

from quast.models.Question import Question


class Tag:
    """Class representing a tag."""

    def __init__(self, name: str, description: str,
                 pool: ThreadedConnectionPool) -> (None):
        self._name = name
        self._description = description
        self._pool = pool

    @staticmethod
    def from_name(name: str, pool: ThreadedConnectionPool):
        """
        Retrieve information of tag ``name`` and return a ``Tag`` object.
        """
        connection = pool.getconn()
        with connection.cursor() as curs:
            curs.execute(
                "SELECT description FROM tags WHERE name=%s", (name, ))
            (description, ) = curs.fetchone()
        pool.putconn(connection)
        return Tag(name=name, description=description, pool=pool)

    @staticmethod
    def create(name: str, description: str, pool: ThreadedConnectionPool):
        """
        Create a new tag and store the information in db.
        """
        conn = pool.getconn()
        with conn.cursor() as curs:
            curs.execute("INSERT INTO tags(name, description) VALUES(%s, %s)",
                         (name, description))
        conn.commit()
        pool.putconn(conn)
        return Tag(name=name, description=description, pool=pool)

    def questions(self):
        """
        Returns questions that are tagged with this tag.
        """
        conn = self._pool.getconn()
        with conn.cursor() as curs:
            curs.execute("SELECT qid FROM question_tags WHERE tag=%s",
                         (self._name, ))
            questions = []
            for qid in curs:
                questions.append(Question.from_qid(qid=qid, pool=self._pool))
        self._pool.putconn(conn)

        return questions

    def as_dict(self):
        """
        Return all the relevant information that ``Tag`` is withholding in form
        of dict.
        """
        return {
            'name': self._name,
            'description': self._description,
        }

    def __eq__(self, other):
        return (
            self._name == other._name and
            self._description == other._description
        )

    @staticmethod
    def search(name, pool):
        conn = pool.getconn()
        results = []
        with conn.cursor() as curs:
            curs.execute("SELECT name FROM tags WHERE name LIKE CONCAT(%s, '%%')", (name, ))
            for (tname, ) in curs:
                results.append(tname)
        pool.putconn(conn)
        return results
