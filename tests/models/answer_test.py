from quast.models.Answer import Answer

from tests.Base import QuastTestCase

class AnswerTest(QuastTestCase):
    def test_from_qid_author(self):
        answer = Answer.from_qid_author(author='raj.mm', qid=1, pool=self.pool)
        self.assertEqual(
            answer._body,
            'You shouldn\'t! Use python, it is damn good, smaller '
            'and beautiful code'
        )

    def test_as_dict(self):
        answer = Answer.from_qid_author(author='raj.mm', qid=1, pool=self.pool)
        self.assertEqual({
            'author': 'raj.mm',
            'body': 'You shouldn\'t! Use python, it is damn good, smaller '
                    'and beautiful code',
            'upvotes': 10000,
            'downvotes': 0,
            'qid': 1
        },
        answer.as_dict())

    def test_delete(self):
        answer = Answer.from_qid_author(author='raj.mm', qid=1, pool=self.pool)
        assert answer.delete()
        with self.assertRaises(TypeError):
            answer = Answer.from_qid_author(author='raj.mm', qid=1, pool=self.pool)

    def test_repr(self):
        answer = Answer.from_qid_author(author='raj.mm', qid=1, pool=self.pool)
        self.assertEqual(repr(answer), '<Answer (qid=1, author=raj.mm)>')

    def test_create(self):
        answer = Answer.create(qid=1, body='test', author='vignesh.vaid', pool=self.pool)
        answer_fetched = Answer.from_qid_author(qid=1, author='vignesh.vaid', pool=self.pool)
        self.assertEqual(answer_fetched, answer)
