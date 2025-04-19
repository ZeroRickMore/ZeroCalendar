import requests

BASE_URL = 'http://localhost:8030/'

def generate_form_data():
    return {
        'title' : 'test',
        'day' : '2025-04-19',
        'when' : '17:35',
        'description' : 'Test culone'
    }

def insert(form_data : dict):
    '''
    title,
    day,
    when,
    description,
    '''

    res = requests.post(BASE_URL+'add_event', data=form_data)

    print(res.text)


def modify(event_id : int, form_data : dict):
    res = requests.post(BASE_URL+f'modify_event/{event_id}', data=form_data)

    print(res.text)


def delete(event_id : int):
    res = requests.get(BASE_URL+f'delete_event/{event_id}')

    print(res.text)


