# ===========================================
#               DATABASE STUFF
# ===========================================
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time

db = SQLAlchemy()

class DayEvent(db.Model):
    __tablename__ = 'day_events'
    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username : str = db.Column(db.String(50), nullable=False)
    created_at : datetime = db.Column(db.DateTime, default=datetime.now)
    title : str= db.Column(db.String(100), nullable=False) #  By default the first 5 words of the desc, up to 100 chars.
    day : date = db.Column(db.Date, nullable=False)
    when : time = db.Column(db.Time, nullable=True)
    description : str = db.Column(db.Text, nullable=False)
    old_version : str= db.Column(db.Text, default='Nessuna versione precedente.', nullable=False)
    last_modified_desc : str = db.Column(db.Text, default='', nullable=False)
    deleted : bool = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<DayEvent id [ {self.id} ] of user [ {self.username} ] created_at [ {self.created_at} ] of title [ {self.title} ] on day [ {self.day} ] and hour [ {self.when} ], of desc [ {self.description} ], old_version [ {self.old_version} ] and last_modified_desc [ {self.last_modified_desc} ]>'
