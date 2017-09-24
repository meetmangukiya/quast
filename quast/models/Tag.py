from psycopg2.pool import ThreadedConnectionPool

class Tag:
    """
    Class representing a tag.
    """

    def __init__(self, name: str, description: str, pool: ThreadedConnectionPool):
        self._name = name
        self._description = description
        self._pool = pool

    @staticmethod
    def from_name(name: str, pool: ThreadedConnectionPool):
        connection = pool.getconn()
        with connection.cursor() as curs:
            curs.execute("SELECT description WHERE name=%s", (name, ))
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

    def as_dict(self):
        return {
            'name': self._name,
            'description': self._description,
        }
