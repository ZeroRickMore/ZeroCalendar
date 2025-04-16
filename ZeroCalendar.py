from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===========================================
#               DATABASE STUFF
# ===========================================

# Define User model
# class User(db.Model):
#     __tablename__ = 'users'
#     name = db.Column(db.String(50), primary_key=True, nullable=False)
#     session_cookie = db.Column(db.String(100), default=None, nullable=True, unique=True)
#     created_at = db.Column(db.DateTime, default=datetime.now)

#     # Relationship to day_events (One-to-many)
#     events = db.relationship('DayEvent', backref='user', lazy=True)

#     def __repr__(self):
#         return f'<User name={self.name}, sc={self.session_cookie}, created_at={self.created_at}>'

# User is a little too advanced, I do not need stuff like that.
# Considering how lazy the users are, and the little scope, an IP address check
# Is more than enough... 

# Define DayEvent model
class DayEvent(db.Model):
    __tablename__ = 'day_events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(100), nullable=True) # By default the first 5 words of the desc, up to 100 chars
    day = db.Column(db.Date, nullable=False)
    when = db.Column(db.Time, nullable=True)
    description = db.Column(db.Text, nullable=False)
    old_version = db.Column(db.Text, default='Nessuna versione precedente.', nullable=False)
    last_modified_desc = db.Column(db.Text, nullable=True) # A column containing stuff like MODIFIED BY Rick, {datetime}

    def __repr__(self):
        return f'<DayEvent {self.day} at {self.when} for user {self.username} of title {self.title} and desc {self.description}>'
    

# ====================================
#               ROUTES
# ====================================


# ====================================
#           EVENT MODIFIERS
# ====================================

@app.route('/add_event')
def add_event():
    '''
    Add an event, via a POST request
    containing:

    title = A max 100 chars string. By default the first 5 words of the desc, up to 100 chars.
    day = Date
    when = Time, in 24h format
    description = Generic text
    
    The username is inferred from the usernames.json
    '''
    pass



@app.route('/modify_event')
def modify_event():
    '''
    Modify an event, via a POST request
    containing:

    title = A max 100 chars string. By default the first 5 words of the desc, up to 100 chars.
    day = Date
    when = Time, in 24h format
    description = Generic text
    
    The username is inferred from the usernames.json
    '''
    pass



@app.route('/delete_event')
def delete_event():
    '''
    Delete an event.
    This is a simple GET request, only user with the same name of the owner
    can delete it.
    
    '''
    pass


# ====================================
#              VISUALIZE
# ====================================



@app.route('/view_event')
def view_event():
    pass



@app.route('/view_day')
def view_day():
    pass






























































if __name__ == '__main__':
    app.run(port=8030, debug=True)