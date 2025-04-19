from flask import Flask, request, jsonify
from models import db, DayEvent
import support


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