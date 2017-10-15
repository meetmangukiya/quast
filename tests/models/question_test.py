from psycopg2 import ProgrammingError

from quast.models.Question import Question
from tests.Base import QuastTestCase


class QuestionTest(QuastTestCase):
    def test_from_qid(self):
        question = Question.from_qid(1, self.pool)
        self.assertEqual(question._author, 'meetmangukiya')

    def test_create(self):
        created = Question.create(title='test question', body='test body',
                                   author='meetmangukiya', tags=[],
                                   pool=self.pool)
        retrieved = Question.from_qid(created._qid, pool=self.pool)
         # import pdb; pdb.set_trace()
        self.assertEqual(retrieved, created)

    def test_answers(self):
        question = Question.from_qid(1, self.pool)
        self.assertEqual(len(question.answers()), 2)

    def test_as_dict(self):
        question = Question.from_qid(1, self.pool)
        self.assertEqual({
            'title': 'Why should we use java for our backend?',
            'description': '',
            'upvotes': 10,
            'downvotes': 2,
            'author': 'meetmangukiya',
            'qid': 1,
            'tags': ['java', 'backend']
        },
        question.as_dict())

    def test_delete(self):
        question = Question.from_qid(1, self.pool)
        assert question.delete()
        with self.assertRaises(TypeError):
            Question.from_qid(1, self.pool)

    def test_repr(self):
        question = Question.from_qid(1, self.pool)
        self.assertEqual('<Question: (qid=1)>', repr(question))
