from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    session_cookie = db.Column(db.String(100), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship to day_events (One-to-many)
    events = db.relationship('DayEvent', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    

# Define DayEvent model
class DayEvent(db.Model):
    __tablename__ = 'day_events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(100), nullable=True) # By default the first 5 words of the desc, up to 100 chars
    day = db.Column(db.Date, nullable=False)
    when = db.Column(db.Time, nullable=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<DayEvent {self.day} at {self.when} for user {self.user_id} of title {self.title} and desc {self.description}>'