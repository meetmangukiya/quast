import os
import unittest

import psycopg2
from psycopg2.pool import ThreadedConnectionPool

class QuastTestCase(unittest.TestCase):
    def setUp(self):
        self.createdb('quast_test')

        # Run setup.sql
        file_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'setup.sql'))
        self.conn = psycopg2.connect("user=postgres dbname=quast_test")
        self.conn.autocommit = True
        with open(file_path) as f:
            with self.conn.cursor() as curs:
                sql = f.read()
                curs.execute(sql)

        # Run populate.sql
        file_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'populate.sql'))
        with open(file_path) as f:
            with self.conn.cursor() as curs:
                sql = f.read()
                curs.execute(sql)

        self.pool = ThreadedConnectionPool(1, 10,
                                           "user=postgres dbname=quast_test")

    @staticmethod
    def createdb(name):
        conn = psycopg2.connect("user=postgres dbname=postgres")
        conn.autocommit = True
        with conn.cursor() as curs:
            curs.execute("CREATE DATABASE {};".format(name))

    @staticmethod
    def dropdb(name):
        conn = psycopg2.connect("user=postgres dbname=postgres")
        conn.autocommit = True
        with conn.cursor() as curs:
            curs.execute("DROP DATABASE {};".format(name))

    def tearDown(self):
        self.pool.closeall()
        self.conn.close()
        self.dropdb('quast_test')
