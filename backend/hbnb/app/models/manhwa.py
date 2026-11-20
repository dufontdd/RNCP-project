# app/models/manhwa.py

from .base_model import BaseModel, db
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

# Table d'association Manhwa <-> Genre
manhwa_genre = Table(
    "manhwa_genre",
    db.metadata,
    Column("manhwa_id", String(60), ForeignKey("manhwas.id"), primary_key=True),
    Column("genre_id", String(60), ForeignKey("genres.id"), primary_key=True)
)

class Manhwa(BaseModel):
    __tablename__ = "manhwas"

    title = Column(String(256), nullable=False)
    synopsis = Column(String)
    author = Column(String(128))
    cover_url = Column(String(512))
    status = Column(String(32))          # ex: ongoing, completed
    chapters = Column(Integer)
    # price, latitude, longitude sont supprimés

    # Relationships
    reviews = relationship("Review", back_populates="manhwa", cascade="all, delete-orphan")
    genres = relationship("Genre", secondary=manhwa_genre, back_populates="manhwas")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "synopsis": self.synopsis,
            "author": self.author,
            "cover_url": self.cover_url,
            "status": self.status,
            "chapters": self.chapters
        }
