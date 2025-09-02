from extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "password": self.password,
        }
