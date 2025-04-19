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
        return f'<DayEvent\n- id [ {self.id} ]\n- user [ {self.username} ]\n- created_at [ {self.created_at} ]\n- title [ {self.title} ]\n- day [ {self.day} ]\n- when [ {self.when} ]\n- desc [\n{self.description}\n\t],\n- old_version [\n{self.old_version}\n\t],\n- last_modified_desc [\n{self.last_modified_desc}\n\t].\n-Deleted {self.deleted}\n>'
