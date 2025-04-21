from datetime import datetime
import json

def get_user(request):
    '''
    Infer the user using usernames.json
    '''
    
    with open("usernames.json", "r") as file:
        data = json.loads(file)

    username = str(data.get(request.remote_addr))

    return username if username is not None else str(request.remote_addr)

    
def get_current_timestamp_string():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y - %H:%M")
    return formatted_time

