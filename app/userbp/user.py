from flask_login import UserMixin

from sqlalchemy import select, insert
from app.database import get_db, users

class User(UserMixin):
    def __init__(self, name, email, profile_pic):
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def get_id(self):
        try:
            return str(self.email)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    @staticmethod
    def get(email):
        db = get_db()
        sql = select(users).where(users.c.email == email)
        user = db.execute(sql).fetchone()

        if not user:
            return None

        user = User(name=user.name, email=user.email, profile_pic=user.profile_pic)
        return user

    @staticmethod
    def create(name, email, profile_pic):
        db = get_db()
        sql = insert(users).values(
            name=name,
            email=email,
            profile_pic=profile_pic,
        )
        db.execute(sql)
        db.commit()