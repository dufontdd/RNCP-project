# app/models/genre.py

from .base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Genre(BaseModel):
    __tablename__ = "genres"

    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(256))

    manhwas = relationship(
        "Manhwa",
        secondary="manhwa_genre",
        back_populates="genres"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
