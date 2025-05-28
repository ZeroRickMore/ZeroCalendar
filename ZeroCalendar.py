from flask import Flask, request, render_template, redirect, url_for
from models import db, DayEvent
from parsers import parse_and_get_DayEvent_object_from_dict, get_DayEvent_dict_from_request_form
from validators import DayEvent_validator
from support import get_user, get_current_timestamp_string
from datetime import datetime, date
import calendar
from loggers import database_logger, myflask_logger
import os
import json

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(flask_app) # Connect to db

# ====================================
#            STARTUP STUFF
# ====================================

def main(DEBUG : bool):
    # Create missing files if necessary
    check_usernames_json()
    check_db()

    # Start server
    create_flask_routes_after_main(DEBUG=DEBUG)
    if DEBUG:
        s = "-----------------< FLASK STARTED IN DEBUG MODE >-----------------"
        myflask_logger.info(s)
        print(s)
        
        flask_app.run(port=8030, debug=True)
    else:
        s = "-----------------< FLASK STARTED >-----------------"
        myflask_logger.info(s)
        print(s)

        flask_app.run(host='0.0.0.0', port=8030, debug=False)

def check_usernames_json():
    # Create usernames.json
    if not os.path.exists('usernames.json'):
        with open('usernames.json', 'w') as f:
            json.dump({}, f)
        myflask_logger.warning(f"Created empty usernames.json file")

def check_db():
    # Create db
    if not os.path.exists(os.path.join('instance', 'sqlite.db')):
        with flask_app.app_context():
            db.create_all()
        myflask_logger.warning(f"Created empty DATABASE instance/sqlite.db")




def create_flask_routes_after_main(DEBUG : bool):
    '''
    This function helps creating the routes only after main() function is called.
    This doesn't look too clean, but it does the job at the cost of just an extra indentation...
    '''

    # ====================================
    #               ROUTES
    # ====================================

    if DEBUG:
        @flask_app.route('/ping')
        def ping():
            myflask_logger.info("Who dares pinging me?!")
            return 'pong'

    # ====================================
    #           EVENT MODIFIERS
    # ====================================

    @flask_app.route('/add_event', methods=['GET', 'POST'])
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
        

        input_data = get_DayEvent_dict_from_request_form(request=request, form_data=request.form)

        new_day_event : DayEvent = parse_and_get_DayEvent_object_from_dict(d = input_data)
        
        db.session.add(new_day_event)
        db.session.commit()

        database_logger.info(f"ADDED EVENT -> {repr(new_day_event.log())}")

        # return {'status': 'success', 'id': new_day_event.id}, 201
        return redirect(url_for('view_day', day=new_day_event.day.day, month=new_day_event.day.month, year=new_day_event.day.year))


    @flask_app.route('/add_event/<int:year>-<int:month>-<int:day>', methods=['GET'])
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
            err = f"All must be int: {type(year)}, {type(month)}, {type(day)}"
            myflask_logger.error(err)
            raise TypeError(err)

        return render_template('add_event.html', today=datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date())

    @flask_app.route('/modify_event/<int:event_id>', methods=['POST'])
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
            err = f"event_id must be int: {type(event_id)}"
            myflask_logger.error(err)
            raise TypeError(err)
        
        input_data = get_DayEvent_dict_from_request_form(request=request, form_data=request.form)
        
        to_be_modified_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

        if to_be_modified_event is None:
            err = f"Event to modify not found with id={event_id}..."
            myflask_logger.error(err)
            raise Exception(err)

        # Save for logger
        previous_stuff = to_be_modified_event.copy()

        username = get_user(request=request)

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

        database_logger.info(f"BEFORE -> {repr(previous_stuff.log())} || AFTER -> {repr(to_be_modified_event.log())}")

        return redirect(url_for('view_day', day=to_be_modified_event.day.day, month=to_be_modified_event.day.month, year=to_be_modified_event.day.year))


    @flask_app.route('/delete_event/<int:event_id>', methods=['GET'])
    def delete_event(event_id):
        '''
        Delete an event by its id.
        This is a simple GET request, no checks whatsoever.

        The element is not really deleted... It just doesn't flask_appear anymore normally.
        Consider it to go to a trash bin.
        '''

        if not isinstance(event_id, int):
            err = f"event_id must be int: {type(event_id)}"
            myflask_logger.error(err)
            raise TypeError(err)
        
        to_be_deleted_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

        to_be_deleted_event.deleted = True

        db.session.commit()

        to_be_deleted_event = db.session.get(DayEvent, event_id) # TODO DEBUG

        database_logger.info(f"DELETED EVENT -> {repr(to_be_deleted_event.log())}")

        # return {'status': 'success', 'deleted_item ': to_be_deleted_event.__repr__()}, 201

        return redirect(url_for('view_day', day=to_be_deleted_event.day.day, month=to_be_deleted_event.day.month, year=to_be_deleted_event.day.year))



    # ====================================
    #              VISUALIZE
    # ====================================



    @flask_app.route('/view_event/<int:event_id>', methods=['GET'])
    def view_event(event_id):
        '''
        View an event by id
        '''
        if not isinstance(event_id, int):
            err = f"event_id must be int: {type(event_id)}"
            myflask_logger.error(err)
            raise TypeError(err)  

        to_be_viewed_event = db.session.get(DayEvent, event_id) # Find item to modify if exists

        return to_be_viewed_event.__repr__()

    @flask_app.route('/view_day/<int:day>-<int:month>-<int:year>', methods=['GET'])
    def view_day(day, month, year):
        '''
        View all events in a day.
        '''
        if not isinstance(day, int):
            err = f"day must be str, not {type(day)}"
            myflask_logger.error(err)
            raise TypeError(err)
        if not isinstance(month, int):
            err = f"day must be str, not {type(month)}"
            myflask_logger.error(err)
            raise TypeError(err)
        if not isinstance(year, int):
            err = f"day must be str, not {type(year)}"
            myflask_logger.error(err)
            raise TypeError(err)


        target_day = date(year, month, day)

        day_objects = db.session.query(DayEvent).filter(DayEvent.deleted == False, DayEvent.day == target_day).order_by('when').all()

        # return escape(str(day_objects) + f'\n\nA TOTAL OF {len(day_objects)}')
        return render_template('view_day.html', 
                            day=day, 
                            month=month, 
                            year=year, 
                            day_objects=day_objects
        )


    @flask_app.route('/')
    def index():
        today = datetime.today()
        current_year = today.year
        current_month = today.month

        return redirect(url_for('view_month', year=current_year, month=current_month))



    @flask_app.route('/view_month/<int:year>-<int:month>')
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

        return render_template('view_month.html', 
                            year=year,
                            month=month,
                            day_numbers=day_numbers_dict,
                            months=['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'],
                            years=range(2025, 2041)
        )




# ====================================
#           LOG PROCESS DEATH
# ====================================


def handle_exit_sigint():
    s = "-------!!!-------< FLASK SHUTTING DOWN (ctrl+c) >-------!!!-------"
    myflask_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)

def handle_exit_sigterm():
    s = "-------!!!-------< FLASK SHUTTING DOWN (systemctl or kill) >-------!!!-------"
    myflask_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)


if __name__ == '__main__':
    main()