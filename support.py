from datetime import datetime

def get_user(catcher = None):
    if catcher is None:
        raise Exception("CAUGHT!")
    
    username = None

    if username is None:
        raise Exception("Fatal error. Who the hell is trying to use the service??!!")

    
def get_current_timestamp_string():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y - %H:%M")
    return formatted_time

