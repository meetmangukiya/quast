import unittest

from psycopg2.pool import ThreadedConnectionPool

from quast.models.Question import Question
from quast.models.Tag import Tag

from tests.Base import QuastTestCase

class TestTag(QuastTestCase):
    def test_from_name(self):
        tag = Tag.from_name('java', self.pool)
        self.assertEqual(tag._name, 'java')
        self.assertEqual(tag._description,
                         'java is one of the most popular programming '
                         'languages.')

    def test_create(self):
        Tag.create('test_tag', 'description', self.pool)
        retrieved_tag = Tag.from_name('test_tag', self.pool)
        expected_tag = Tag('test_tag', 'description', self.pool)
        self.assertEqual(retrieved_tag, expected_tag)

    def test_questions(self):
        tag = Tag.create(name='test_tag', description='..', pool=self.pool)
        question = Question.create(title='asa', author='meetmangukiya', body='',
                                   tags=['test_tag'], pool=self.pool)
        self.assertEqual(len(tag.questions()), 1)

    def test_as_dict(self):
        tag = Tag.from_name('java', self.pool)
        self.assertEqual({'name': 'java',
                          'description': 'java is one of the most popular '
                                         'programming languages.'},
                         tag.as_dict())

    def test_tag_search(self):
        tags = Tag.search('j', self.pool)
        self.assertEqual(tags, ['java'])
