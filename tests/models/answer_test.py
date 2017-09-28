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