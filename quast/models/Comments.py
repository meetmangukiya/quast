from quast.models.User import User


class Comment:
    """
    Class representing a comment.
    """

    def __init__(self,
                 author: User,
                 upvotes: int,
                 downvotes: int,
                 body: str) -> (None):
        self._author = author
        self._upvotes = upvotes
        self._downvotes = downvotes
        self._body = body


class QuestionComment(Comment):
    """
    Class representing a question comment.
    """

    def __init__(self,
                 author: User,
                 upvotes: int,
                 downvotes: int,
                 body: str,
                 qid: int) -> (None):
        super().__init__(author=author, upvotes=upvotes, downvotes=downvotes,
                         body=body)
        self._qid = qid


class AnswerComment(Comment):
    """
    Class representing an answer comment.
    """

    def __init__(self,
                 author: User,
                 upvotes: int,
                 downvotes: int,
                 body: str,
                 qid: int,
                 aid: int) -> (None):
        super().__init__(author=author, upvotes=upvotes, downvotes=downvotes,
                         body=body)
        self._aid = aid
        self._qid = qid
