# ====================================
#              PARSING
# ====================================

from models import DayEvent
from validators import DayEvent_validator
from datetime import datetime
from support import get_user

def get_DayEvent_dict_from_request_form(form_data):
    input_data = {
        'username' : get_user(),
        'description' : form_data.get('description'),
        'title' : form_data.get('title'),
        'old_version' : form_data.get('old_version'),
        'last_modified_desc' : form_data.get('last_modified_desc'),
        'day' : datetime.strptime(form_data.get('day'), '%Y-%m-%d').date() if form_data.get('day') else None, # Format day
        'when' : datetime.strptime(form_data.get('when'), '%H:%M').time() if form_data.get('when') else None, # Format when
    }

    return input_data

def parse_and_get_DayEvent_object_from_dict(d : dict = None):    
    '''
    Takes a dictionary containing:

        username,
        title,
        day,
        when,
        description,
        old_version,
        last_modified_desc,

    And returns a DayEvent object filled with them.
    (id and created_at are autofilled when inserted into the db by Flask)

    Can raise KeyError, TypeError, ValueError mainly.
    '''
    if not isinstance(d, dict):
        raise ValueError(f"\nd must be a Dictionary, not {type(d)}")

    day_event = DayEvent()

    # Throws KeyError if it's not present (it should be...)
    day_event.username = d['username']
    day_event.description = d['description']
    day_event.title = d['title']
    day_event.old_version = d['old_version']
    day_event.last_modified_desc = d['last_modified_desc']
    day_event.day = d['day']
    day_event.when = d.get('when') # None is fine too

    DayEvent_validator(day_event=day_event)

    return day_event