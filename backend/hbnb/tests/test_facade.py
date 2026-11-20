# tests/test_facade.py
import unittest
from app import create_app
from app.models.base_model import db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class TestFacade(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.facade = self.app.facade

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_user(self):
        user = self.facade.create_user({
            "email": "test@example.com",
            "password": "1234",
            "first_name": "Test",
            "last_name": "User"
        })
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")
        self.assertNotEqual(user.password, "1234")  # le mot de passe doit être hashé

    def test_create_genre(self):
        genre = self.facade.create_genre({"name": "Action"})
        self.assertIsNotNone(genre.id)
        self.assertEqual(genre.name, "Action")

    def test_create_manhwa(self):
        manhwa = self.facade.create_manhwa({
            "title": "Solo Leveling",
            "author": "Chugong",
            "description": "Un chasseur très faible devient le plus puissant."
        })
        self.assertIsNotNone(manhwa.id)
        self.assertEqual(manhwa.title, "Solo Leveling")

    def test_create_review(self):
        user = self.facade.create_user({
            "email": "r@example.com", "password": "1234",
            "first_name": "R", "last_name": "R"
        })
        manhwa = self.facade.create_manhwa({
            "title": "Tower of God", "author": "SIU", "description": "..."
        })
        review = self.facade.create_review({
            "text": "Super !", "rating": 5,
            "user_id": user.id, "manhwa_id": manhwa.id
        })
        self.assertIsNotNone(review.id)
        self.assertEqual(review.rating, 5)

    def test_get_lists(self):
        self.facade.create_genre({"name": "Fantasy"})
        self.assertEqual(len(self.facade.get_genres()), 1)
        self.assertEqual(len(self.facade.get_users()), 0)
        self.assertEqual(len(self.facade.get_manhwas()), 0)


if __name__ == "__main__":
    unittest.main()
