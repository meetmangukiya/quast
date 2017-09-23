from psycopg2.extensions import connection
from psycopg2.pool import ThreadedConnectionPool

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
            curs.execute("SELECT followed_by FROM users "
                         "WHERE following_to=%s", (self._username, ))
            followers = list(map(lambda x: x[0], curs.fetchall()))
        self._pool.putconn(conn)
        return followers
