from flask import Flask, request, render_template
from models import db, DayEvent
from parsers import parse_and_get_DayEvent_object_from_dict, get_DayEvent_dict_from_request_form
from validators import DayEvent_validator
from datetime import datetime, date, time
from support import get_user, get_current_timestamp_string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # Connect to db
    

# ====================================
#               ROUTES
# ====================================


# ====================================
#           EVENT MODIFIERS
# ====================================

@app.route('/add_event', methods=['POST'])
def add_event():
    '''
    Add an event, via a POST request
    containing:

        username,
        title,
        day,
        when,
        description,
        old_version,
        last_modified_desc,
    
    The username is inferred from the usernames.json
    '''

    input_data = get_DayEvent_dict_from_request_form(form_data=request.form)

    new_day_event : DayEvent = parse_and_get_DayEvent_object_from_dict(d = input_data)
    
    db.session.add(new_day_event)
    db.session.commit()

    return {'status': 'success', 'id': new_day_event.id}, 201



@app.route('/modify_event/<int:event_id>', methods=['POST'])
def modify_event(event_id):
    '''
    Modify an event, via a POST request on URL with its ID,
    containing:

        username,
        title,
        day,
        when,
        description,
        old_version,
        last_modified_desc,
    
    The username is inferred from the usernames.json
    '''
    if not isinstance(event_id, int):
        raise TypeError(f"event_id must be int: {type(event_id)}")
    
    
    to_be_modified_event = db.session.get(DayEvent, event_id) # Find item to modify if exists
    old = to_be_modified_event # TODO DEBUG

    if to_be_modified_event is None:
        raise Exception("Event to modify not found...")

    username = get_user()

     # Save old version =============================
    to_be_modified_event.old_version = f'''
- Titolo: <<{to_be_modified_event.title}>>
- Giorno: {to_be_modified_event.day}
- Ora: {to_be_modified_event.when}
- Descrizione:
<<{to_be_modified_event.description}>>
    '''

    to_be_modified_event.last_modified_desc += f"- Modificato da {username} - {get_current_timestamp_string()}\n"
    # ================================================

    input_data = get_DayEvent_dict_from_request_form(form_data=request.form)

    to_be_modified_event.username = username
    to_be_modified_event.description = input_data['description']
    to_be_modified_event.title = input_data['title']
    to_be_modified_event.old_version = input_data['old_version']
    to_be_modified_event.last_modified_desc = input_data['last_modified_desc']
    to_be_modified_event.day = input_data['day']
    to_be_modified_event.when = input_data['when']

    DayEvent_validator(day_event = to_be_modified_event) # Make sure the modifications make sense

    db.session.commit()

    to_be_modified_event = db.session.get(DayEvent, event_id) # TODO DEBUG

    return {'status': 'success', 'old' : old.__repr__(),'new': to_be_modified_event.__repr__()}, 201



@app.route('/delete_event/<int:event_id>', methods=['GET'])
def delete_event(event_id):
    '''
    Delete an event by its id.
    This is a simple GET request, no checks whatsoever.

    The element is not really deleted... It just doesn't appear anymore normally.
    Consider it to go to a trash bin.
    '''

    if not isinstance(event_id, int):
        raise TypeError(f"event_id must be int: {type(event_id)}")
    
    to_be_deleted_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

    old = to_be_deleted_event # TODO DEBUG

    to_be_deleted_event.deleted = True

    db.session.commit()

    to_be_deleted_event = db.session.get(DayEvent, event_id) # TODO DEBUG

    return {'status': 'success', 'old' : old.__repr__(),'new': to_be_deleted_event.__repr__()}, 201



# ====================================
#              VISUALIZE
# ====================================



@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    '''
    View an event by id
    '''
    if not isinstance(event_id, int):
        raise TypeError(f"event_id must be int: {type(event_id)}")  

    to_be_viewed_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

    return to_be_viewed_event.__repr__()

@app.route('/view_day')
def view_day():
    pass






























































if __name__ == '__main__':
    app.run(port=8030, debug=True)