from quast.models.Comments import QuestionComment, AnswerComment

from tests.Base import QuastTestCase

class QuestionCommentTest(QuastTestCase):
    def test_comment(self):
        q_comment = QuestionComment('meetmangukiya', 0, 0, 'question comment', 1)
        a_comment = AnswerComment('meetmangukiya', 0, 0, 'answer comment', 1,
                                  'raj.mm')
