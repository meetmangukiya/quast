from psycopg2.extensions import connection

class User:
    """
    Class representing a User.
    """

    def __init__(self,
                 username: str=None,
                 credits: int=0,
                 bio: str=None):
        self._username = username
        self._credits = int(credits)
        self._bio = str(bio) if bio else ''

    @staticmethod
    def from_username(username: str,
                      conn: connection):
        with conn.cursor() as curs:
            curs.execute("""SELECT username, credits, bio
                         FROM users WHERE username=%s""",
                         (str(username), ))
            username, credits, bio = curs.fetchone()
        return User(username=username, credits=credits, bio=bio)
