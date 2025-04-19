from flask import Flask, request, jsonify
from models import db, DayEvent
from parsers import parse_and_get_DayEvent_object_from_dict
from datetime import datetime, date, time

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
    form_data = request.form

    input_data = {
        'username' : form_data.get('username'),
        'description' : form_data.get('description'),
        'title' : form_data.get('title'),
        'old_version' : form_data.get('old_version'),
        'last_modified_desc' : form_data.get('last_modified_desc'),
        'day' : datetime.strptime(form_data.get('day'), '%Y-%m-%d').date() if form_data.get('day') else None, # Format day
        'when' : datetime.strptime(form_data.get('when'), '%H:%M').time() if form_data.get('when') else None, # Format when
    }

    new_day_event : DayEvent = parse_and_get_DayEvent_object_from_dict(d = input_data)
    
    db.session.add(new_day_event)
    db.session.commit()

    return {'status': 'success', 'id': new_day_event.id}, 201



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