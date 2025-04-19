from datetime import datetime

def get_user(catcher = None):
    '''
    Infer the user using usernames.json
    '''
    if catcher is None:
        raise Exception("CAUGHT!")
    
    username = None
    username = 'TEST'

    if username is None:
        raise Exception("Fatal error. Who the hell is trying to use the service??!!")
    
    return username

    
def get_current_timestamp_string():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y - %H:%M")
    return formatted_time

