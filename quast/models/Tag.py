from psycopg2.extensions import connection

class Tag:
    """
    Class representing a tag.
    """

    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description

    @staticmethod
    def from_name(name: str, conn: connection):
        with connection.cursor() as curs:
            curs.execute("SELECT description WHERE name=%s", (name, ))
            (description, ) = curs.fetchone()
        return Tag(name=name, description=description)
