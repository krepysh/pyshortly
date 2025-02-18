from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    @property
    def is_active(self):
        return True

    @property
    def user_name(self):
        return self.username

    def get_id(self) -> str:
        return self.username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class Url(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column()
    hash_id: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    views: Mapped[int] = mapped_column(default=0)
