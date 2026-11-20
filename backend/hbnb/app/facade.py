# app/facade.py

from app.models.base_model import db
from app.models.user import User
from app.models.manhwa import Manhwa
from app.models.genre import Genre
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ManhwaFacade:
    """Façade pour gérer les opérations CRUD sur Users, Manhwas, Genres et Reviews"""

    def __init__(self):
        # Repository SQLAlchemy avec la session de la base
        self.repo = SQLAlchemyRepository(db.session)

    # ---------------- USERS ----------------
    def create_user(self, data):
        if self.get_user_by_email(data.get("email")):
            raise ValueError("email already registered")
        user = User(**data)
        return self.repo.add(user)

    def get_users(self):
        return self.repo.get_all(User)

    def get_user(self, user_id):
        return self.repo.get(User, user_id)

    def get_user_by_email(self, email):
        return self.repo.get_by_email(User, email)

    def update_user(self, obj_id, data):
        user = self.get_user(obj_id)
        if not user:
            return None
        if "email" in data and data["email"] != user.email:
            if self.get_user_by_email(data["email"]):
                raise ValueError("email already registered")
        for key, value in data.items():
            setattr(user, key, value)
        return self.repo.update(user)

    def delete_user(self, obj_id):
        user = self.get_user(obj_id)
        if not user:
            return False
        self.repo.delete(user)
        return True

    # ---------------- MANHWAS ----------------
    def create_manhwa(self, data):
        required_fields = ["title", "author"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is required")
        genre_ids = data.pop("genre_ids", [])
        manhwa = Manhwa(**data)
        for genre_id in genre_ids:
            genre = self.get_genre(genre_id)
            if not genre:
                raise ValueError(f"genre {genre_id} does not exist")
            manhwa.genres.append(genre)
        return self.repo.add(manhwa)

    def get_manhwas(self):
        return self.repo.get_all(Manhwa)

    def get_manhwa(self, manhwa_id):
        return self.repo.get(Manhwa, manhwa_id)

    def update_manhwa(self, obj_id, data):
        manhwa = self.get_manhwa(obj_id)
        if not manhwa:
            return None
        genre_ids = data.pop("genre_ids", None)
        for key, value in data.items():
            setattr(manhwa, key, value)
        if genre_ids is not None:
            manhwa.genres = []
            for genre_id in genre_ids:
                genre = self.get_genre(genre_id)
                if not genre:
                    raise ValueError(f"genre {genre_id} does not exist")
                manhwa.genres.append(genre)
        return self.repo.update(manhwa)

    def delete_manhwa(self, obj_id):
        manhwa = self.get_manhwa(obj_id)
        if not manhwa:
            return False
        self.repo.delete(manhwa)
        return True

    # ---------------- GENRES ----------------
    def create_genre(self, data):
        genre = Genre(**data)
        return self.repo.add(genre)

    def get_genres(self):
        return self.repo.get_all(Genre)

    def get_genre(self, genre_id):
        return self.repo.get(Genre, genre_id)

    def update_genre(self, obj_id, data):
        genre = self.get_genre(obj_id)
        if not genre:
            return None
        for key, value in data.items():
            setattr(genre, key, value)
        return self.repo.update(genre)

    def delete_genre(self, obj_id):
        genre = self.get_genre(obj_id)
        if not genre:
            return False
        self.repo.delete(genre)
        return True

    # ---------------- REVIEWS ----------------
    def create_review(self, data):
        review = Review(**data)
        return self.repo.add(review)

    def get_reviews(self):
        return self.repo.get_all(Review)

    def get_review(self, obj_id):
        return self.repo.get(Review, obj_id)

    def update_review(self, obj_id, data):
        review = self.get_review(obj_id)
        if not review:
            return None
        for key, value in data.items():
            setattr(review, key, value)
        return self.repo.update(review)

    def delete_review(self, obj_id):
        review = self.get_review(obj_id)
        if not review:
            return False
        self.repo.delete(review)
        return True

    # ---------------- Review convenience ----------------
    def get_review_by_user_and_manhwa(self, user_id, manhwa_id):
        return self.repo.get_review_by_user_and_manhwa(user_id, manhwa_id)
