from app.db import db

import datetime


class Recommendations(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    diet = db.Column(db.String(255), nullable=True)
    exercises = db.Column(db.String(255), nullable=True)
    dietRecommendedAt = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    exerciseRecommendedAt = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    user = db.relationship('User', backref=db.backref('recommendations', lazy=True))