from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

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
