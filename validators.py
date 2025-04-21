
from models import DayEvent
from datetime import date, time

def DayEvent_validator(day_event : DayEvent) -> bool:
    '''
    Raises TypeError or ValueError if validation fails.
    Returns True if validation is successful.

    Also, fills in the Title field automatically.
    '''
    if not isinstance(day_event, DayEvent):
        raise TypeError(f"day_event is not DayEvent: {type(d)}")
    
    # Username ====================================================

    username = day_event.username

    if not isinstance(username, str):
        raise TypeError(f"\nUsername is not str: {type(username)}")
    if len(username) > 50:
        raise ValueError(f"\nUsername length is too much: {len(username)} > 50.")


    # Description ====================================================

    desc = day_event.description

    if not isinstance(desc, str):
        raise TypeError(f"\nDescription is not str: {type(desc)}")

    # Title ====================================================

    title = day_event.title

    if not isinstance(title, str):
        raise TypeError(f"\nTitle is not str: {type(title)}")
    
    if len(title) > 100:
        raise ValueError(f"\nTitle length is too much: {len(title)} > 100.")

    if len(title) == 0:
        print("\nTitle was not given. Taking first 100 char of description for it.")

        if len(desc) == 0:
            raise ValueError(f"\nDescription or title must be given, they can not be both empty strings!")
    
        temp = day_event.description
        temp = temp.split(" ")
        for word in temp:
            test = day_event.title + word
            if len(test) > 100:
                break
            day_event.title += word + ' '

    # Old_version ====================================================

    old_version = day_event.old_version

    if not isinstance(old_version, str):
        raise TypeError(f"\nOld_version is not str: {type(old_version)}")

    # Last_modified_desc ====================================================

    last_modified_desc = day_event.last_modified_desc

    if not isinstance(last_modified_desc, str):
        raise TypeError(f"\nLast_modified_desc is not str: {type(last_modified_desc)}")

    # Day ====================================================

    day = day_event.day

    if not isinstance(day, date):
        raise TypeError(f"\nday is not date: {type(day)}")
    
    if day.year < 2025:
        raise ValueError(f"Year must be >= 2025: {day.year}")
    
    if day.year > 2040:
        raise ValueError(f"Year must be <= 2040: {day.year}")

    # When ====================================================

    when = day_event.when

    if not isinstance(when, time) and when is not None:
        raise TypeError(f"\nwhen is not time nor None: {type(when)}")

    if when.hour not in range(0, 24):
        raise ValueError(f"Hour must be in 0-23 range: {when.hour}")
    
    if when.minute not in range(0, 60):
        raise ValueError(f"Min must be in 0-59 range: {when.minute}")

    return True