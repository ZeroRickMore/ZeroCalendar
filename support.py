# ====================================
#              PARSING
# ====================================

from models import DayEvent
from datetime import datetime, date, time

'''
    __tablename__ = 'day_events'
    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username : str = db.Column(db.String(50), nullable=False)
    created_at : datetime = db.Column(db.DateTime, default=datetime.now)
    title : str= db.Column(db.String(100), nullable=False) #  By default the first 5 words of the desc, up to 100 chars.
    day : date = db.Column(db.Date, nullable=False)
    when : time = db.Column(db.Time, nullable=True)
    description : str = db.Column(db.Text, nullable=False)
    old_version : str= db.Column(db.Text, default='Nessuna versione precedente.', nullable=False)
    last_modified_desc : str = db.Column(db.Text, nullable=True)
'''
def get_DayEvent_object_from_dict(d : dict = None):    
    '''
    Takes a dictionary containing:
        username ,
        title ,
        day ,
        when ,
        description ,
        old_version ,
        last_modified_desc ,

    And returns a DayEvent object filled with them.

    Can raise KeyError, TypeError, ValueError mainly.
    '''
    if not isinstance(d, dict):
        raise ValueError(f"\nd must be a Dictionary, not {type(d)}")

    day_event = DayEvent()
    
    # Username ====================================================

    username = d['username']

    if not isinstance(username, str):
        raise TypeError(f"\nUsername is not str: {type(username)}")
    if len(username) > 50:
        raise ValueError(f"\nUsername length is too much: {len(username)} > 50.")
    day_event.username = username

    # Description ====================================================

    desc = d['description']

    if not isinstance(desc, str):
        raise TypeError(f"\nDescription is not str: {type(desc)}")

    day_event.description = desc


    # Title ====================================================

    title = d['title']

    if not isinstance(title, str):
        raise TypeError(f"\nTitle is not str: {type(title)}")
    
    if len(title) > 100:
        raise ValueError(f"\nTitle length is too much: {len(title)} > 100.")

    if len(title) == 0:
        print("\nTitle was not given. Taking first 100 char of description for it.")
        temp = day_event.description
        temp = temp.split(" ")
        for word in temp:
            test = day_event.title + word
            if len(test) > 100:
                break
            day_event.title += word
    else:
        day_event.title = title

    # Old_version ====================================================

    old_version = d['old_version']

    if not isinstance(old_version, str):
        raise TypeError(f"\nOld_version is not str: {type(old_version)}")

    day_event.old_version = old_version

    # Last_modified_desc ====================================================

    last_modified_desc = d['last_modified_desc']

    if not isinstance(last_modified_desc, str):
        raise TypeError(f"\nLast_modified_desc is not str: {type(last_modified_desc)}")

    day_event.last_modified_desc = last_modified_desc

    # Day ====================================================

    day = d['day']

    if not isinstance(day, date):
        raise TypeError(f"\nday is not date: {type(day)}")

    day_event.day = day

    # When ====================================================

    when = d.get('when') # None is fine too

    if not isinstance(when, time) and when is not None:
        raise TypeError(f"\nwhen is not time nor None: {type(when)}")

    day_event.when = when

    return day_event



get_DayEvent_object_from_dict(d = {'username' : 1})