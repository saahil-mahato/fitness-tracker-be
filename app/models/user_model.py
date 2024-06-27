from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    activityLevel = db.Column(db.String(32), nullable=False)
    isTrainer = db.Column(db.Boolean, default=False)
    passwordHash = db.Column(db.String(128), nullable=False)

    latestExercises = db.Column(db.String(255), nullable=True)
    latestDiet = db.Column(db.String(255), nullable=True)
    
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)