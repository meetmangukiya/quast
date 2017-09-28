from quast.models.User import User

from tests.Base import QuastTestCase

class UserTest(QuastTestCase):
    def test_from_username(self):
        user = User.from_username('meetmangukiya', self.pool)
        self.assertEqual(user._username, 'meetmangukiya')
        self.assertEqual(user._bio, 'aka mangu(forcefully :( ); handles backend')
        self.assertEqual(user._credits, 100)

    def test_get_followers(self):
        user = User.from_username('meetmangukiya', self.pool)
        self.assertEqual(user.get_followers(),
                         ['chintan.gm', 'raj.mm', 'vignesh.vaid'])

    def test_as_dict(self):
        user = User.from_username('meetmangukiya', self.pool)
        self.assertEqual({
            'username': 'meetmangukiya',
            'bio': 'aka mangu(forcefully :( ); handles backend',
            'credits': 100
        }, user.as_dict())

    def test_get_questions(self):
        user = User.from_username('meetmangukiya', self.pool)
        self.assertEqual(len(user.get_questions()), 1)
