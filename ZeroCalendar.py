from flask import Flask, request, render_template, redirect, url_for
from models import db, DayEvent
from parsers import parse_and_get_DayEvent_object_from_dict, get_DayEvent_dict_from_request_form
from validators import DayEvent_validator
from support import get_user, get_current_timestamp_string
from datetime import datetime, date
import calendar
from markupsafe import escape

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # Connect to db

# ====================================
#               ROUTES
# ====================================
    
@app.route('/ping')
def ping():
    return 'pong'


# ====================================
#           EVENT MODIFIERS
# ====================================

@app.route('/add_event', methods=['GET', 'POST'])
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

    if request.method == 'GET':
        return render_template('add_event.html', today=datetime.today())
    

    input_data = get_DayEvent_dict_from_request_form(form_data=request.form)

    new_day_event : DayEvent = parse_and_get_DayEvent_object_from_dict(d = input_data)
    
    db.session.add(new_day_event)
    db.session.commit()

    # return {'status': 'success', 'id': new_day_event.id}, 201
    return redirect(url_for('view_day', day=new_day_event.day.day, month=new_day_event.day.month, year=new_day_event.day.year))


@app.route('/add_event/<int:year>-<int:month>-<int:day>', methods=['GET'])
def add_event_of_day(year, month, day):
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
    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        raise TypeError(f"All must be int: {type(year)}, {type(month)}, {type(day)}")

    return render_template('add_event.html', today=datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date())

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
    
    input_data = get_DayEvent_dict_from_request_form(form_data=request.form)
    
    to_be_modified_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

    if to_be_modified_event is None:
        raise Exception("Event to modify not found...")

    username = get_user()

     # Save old version =============================
    to_be_modified_event.old_version = f'''- Titolo: << {to_be_modified_event.title} >>
- Giorno: {to_be_modified_event.day}
- Ora: {to_be_modified_event.when}
- Descrizione:
<<{to_be_modified_event.description}>>'''

    to_be_modified_event.last_modified_desc += f"- Modificato da {username} - {get_current_timestamp_string()}\n"
    # ================================================

    to_be_modified_event.username = username
    to_be_modified_event.description = input_data['description'].capitalize()
    to_be_modified_event.title = input_data['title'].capitalize()
    to_be_modified_event.day = input_data['day']
    to_be_modified_event.when = input_data['when']

    DayEvent_validator(day_event = to_be_modified_event) # Make sure the modifications make sense

    db.session.commit()

    to_be_modified_event = db.session.get(DayEvent, event_id) # TODO DEBUG

    # return {'status': 'success', 'new': to_be_modified_event.__repr__()}, 201

    return redirect(url_for('view_day', day=to_be_modified_event.day.day, month=to_be_modified_event.day.month, year=to_be_modified_event.day.year))


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

    to_be_deleted_event.deleted = True

    db.session.commit()

    to_be_deleted_event = db.session.get(DayEvent, event_id) # TODO DEBUG

    # return {'status': 'success', 'deleted_item ': to_be_deleted_event.__repr__()}, 201

    return redirect(url_for('view_day', day=to_be_deleted_event.day.day, month=to_be_deleted_event.day.month, year=to_be_deleted_event.day.year))



# ====================================
#              VISUALIZE
# ====================================



@app.route('/view_event/<int:event_id>', methods=['GET'])
def view_event(event_id):
    '''
    View an event by id
    '''
    if not isinstance(event_id, int):
        raise TypeError(f"event_id must be int: {type(event_id)}")  

    to_be_viewed_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

    return to_be_viewed_event.__repr__()

@app.route('/view_day/<int:day>-<int:month>-<int:year>', methods=['GET'])
def view_day(day, month, year):
    '''
    View all events in a day.
    '''
    if not isinstance(day, int):
        raise TypeError(f"day must be str, not {type(day)}")
    if not isinstance(month, int):
        raise TypeError(f"day must be str, not {type(month)}")
    if not isinstance(year, int):
        raise TypeError(f"day must be str, not {type(year)}")
    
    print(day, month, year)

    target_day = date(year, month, day)

    day_objects = db.session.query(DayEvent).filter(DayEvent.deleted == False, DayEvent.day == target_day).order_by('when').all()

    # return escape(str(day_objects) + f'\n\nA TOTAL OF {len(day_objects)}')
    return render_template('view_day.html', 
                           day=day, 
                           month=month, 
                           year=year, 
                           day_objects=day_objects
    )


@app.route('/')
def index():
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    return redirect(url_for('view_month', year=current_year, month=current_month))



@app.route('/view_month/<int:year>-<int:month>')
def view_month(year, month):

    _, day_number = calendar.monthrange(year, month)
    first_weekday_index = calendar.weekday(year, month, 1)
    
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    should_check_past = (current_year == year) and (current_month == month)

    day_numbers = [50+_ for _ in range(first_weekday_index)] + [i for i in range(1, day_number+1)] # Skip to fit monday in column

    day_numbers_dict = {}

    for day_number in day_numbers:
        if day_number >= 50 : # Days to skip
            day_numbers_dict[day_number] = None
        elif should_check_past and day_number < datetime.today().day: # Past day and I should check for it
            day_numbers_dict[day_number] = 'A'
        else:
            target_day = date(year, month, day_number)
            day_numbers_dict[day_number] = db.session.query(DayEvent).filter(DayEvent.deleted == False, DayEvent.day == target_day).count()
    
    print(day_numbers_dict)

    return render_template('view_month.html', 
                           year=year,
                           month=month,
                           day_numbers=day_numbers_dict,
                           months=['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'],
                           years=range(2025, 2041)
    )








































if __name__ == '__main__':
    app.run(port=8030, debug=True)