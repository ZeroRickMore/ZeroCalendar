import ZeroCalendarBot.ZeroCalendarBot as ZeroCalendar_bot
import asyncio
from loggers import scheduler_logger
from models import db, DayEvent
from datetime import datetime, timedelta
import time
from ZeroCalendar import flask_app


# ====================================
#            MAIN METHOD
# ====================================

def main(RUN_ONLY_FIRST_MESSAGE : bool, DO_NOT_SKIP_NIGHT : bool, WAIT_ONLY_1_MINUTE : bool):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    s = f"-----------------< SCHEDULER STARTED >-----------------"
    scheduler_logger.info(s)
    print(s)

    while(True):
        # If it's night time, don't wake everybody up with a message
        sleep_through_the_night(DO_NOT_SKIP_NIGHT=DO_NOT_SKIP_NIGHT)

        # Send morning notification night after the sleep! It makes sense, no fancy controls if it's 10:00 or not
        # because sleep_through_the_night() already handles it
        send_morning_day_events_notification(asyncio_loop=loop)

        if not RUN_ONLY_FIRST_MESSAGE: wait_until_next_quarter(WAIT_ONLY_1_MINUTE=WAIT_ONLY_1_MINUTE) # Align with quarter, so wait 15 minutes
        
        check_next_events(asyncio_loop=loop) # Send the message

        if RUN_ONLY_FIRST_MESSAGE: 
            s = "-------!!!-------< SCHEDULER STOPPED DUE TO DEBUG OPTION ON >-------!!!-------"
            print(s)
            scheduler_logger.warning(s)
            break



# ====================================
#             SLEEP NIGHT
# ====================================


def sleep_through_the_night(DO_NOT_SKIP_NIGHT : bool):
    if DO_NOT_SKIP_NIGHT: return

    now = datetime.now()
    night_start = now.replace(hour=21, minute=0, second=0, microsecond=0)
    wake_time = now.replace(hour=10, minute=0, second=0, microsecond=0)

    if now >= night_start:
        # If after 21:00, sleep until 10:00 AM *tomorrow*
        wake_time += timedelta(days=1)
        sleep_duration = (wake_time - now).total_seconds()
        s = f"Sleeping for {sleep_duration/3600:.2f} hours until {wake_time.strftime('%H:%M')}. GOODNIGHT!"
        scheduler_logger.info(s)
        print(s)
        time.sleep(sleep_duration)
    else:
        s = "It's not night yet — no need to sleep."
        print(s)
        scheduler_logger.info(s)



# ====================================
#                WAIT
# ====================================

def wait_until_next_quarter(WAIT_ONLY_1_MINUTE : bool):
    now = datetime.now()

    multiple_to_align_with = 15 # Should be 15
    if WAIT_ONLY_1_MINUTE: multiple_to_align_with = 1

    minutes_to_wait = multiple_to_align_with - (now.minute % multiple_to_align_with)

    next_quarter = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_wait)
    delay = (next_quarter - now).total_seconds()
    s = f"Waiting {delay/60:.2f} minutes to align with {next_quarter.strftime('%H:%M')}"
    scheduler_logger.info(s)
    print(s)
    time.sleep(delay)



# ====================================
#            CHECK EVENTS
# ====================================

def send_morning_day_events_notification(asyncio_loop) -> None:
    today_from_10_to_midnight_events, tomorrow_from_midnight_to_10 = get_day_events_total()
    s = craft_whole_day_events_notification_text(today_from_10_to_midnight_events=today_from_10_to_midnight_events, tomorrow_from_midnight_to_10=tomorrow_from_midnight_to_10)
    make_bot_write(asyncio_loop=asyncio_loop, text=s)

def check_next_events(asyncio_loop) -> None:
    # Events of the whole day, if morning, are handled in the main loop after sleep_through_the_night()

    # Events of the next hour
    events = get_events_in_next_hour()
    if len(events)>0:  
        s = craft_events_notification_text(events=events)
        make_bot_write(asyncio_loop=asyncio_loop, text=s)




# ====================================
#             GET EVENTS
# ====================================


def get_events_in_next_hour() -> list[DayEvent]:
    '''
    Returns a list of the events within the next hour
    '''
    now = datetime.now()
    today = now.date()
    current_hour = now.time()
    one_hour_later = (now + timedelta(hours=1)).time()

    with flask_app.app_context():
        events : list[DayEvent] = db.session.query(DayEvent).filter(
            DayEvent.deleted == False, 
            DayEvent.day == today,
            DayEvent.when >= current_hour,
            DayEvent.when <= one_hour_later
        ).order_by('when').all()
    
    return events


def get_day_events_total() -> tuple[list[DayEvent], list[DayEvent]] :
    '''
    Returns two lists.
    One is the events that go from today 10:00 AM to midnight.
    The other is the events that go from tomorrow midnight to 10:00 AM.
    '''
    now = datetime.now()
    today = now.date()
    today_start_time = now.replace(hour=10, minute=0, second=0, microsecond=0)

    # Get events from today 10:00 to midnight
    with flask_app.app_context():
        today_from_10_to_midnight_events : list[DayEvent] = db.session.query(DayEvent).filter(
            DayEvent.deleted == False,
            DayEvent.day == today,
            DayEvent.when >= today_start_time, # After 10:00 only
        ).order_by('when').all()
    
    # Get events from tomorrow 00:00 to 10:00
    tomorrow = (now + timedelta(days=1)).date()
    tomorrow_start_time = now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)

    with flask_app.app_context():
        tomorrow_from_midnight_to_10 : list[DayEvent] = db.session.query(DayEvent).filter(
            DayEvent.deleted == False,
            DayEvent.day == tomorrow,
            DayEvent.when <= tomorrow_start_time, # Before 10:00 only
        ).order_by('when').all()    


    return today_from_10_to_midnight_events, tomorrow_from_midnight_to_10  


# ====================================
#            CRAFT MESSAGE
# ====================================

def craft_events_notification_text(events : list[DayEvent]) -> str:
    # Validation
    if not isinstance(events, list):
        err = f"events must be a list, not {type(events)}"
        scheduler_logger.error(err)
        print(err)
        return
        # raise TypeError(err)
    if len(events)==0:
        err = f"Why was this function called with no events? len(events)==0"
        scheduler_logger.error(err)
        print(err)
        return
        # raise ValueError(err)
    
    # Logic
    if len(events)==1:
        s = "*Ciao!* 💜💫\nQuesto è l'evento della prossima ora.\n\n⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\n\n──────────────────────────\n"
    else:
        s = "*Ciao!* 💜💫\nQuesti sono gli eventi della prossima ora.\n\n⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\n\n──────────────────────────\n"

    EVENT_BULLETPOINT = '📝'

    now = datetime.now()

    for event in events:
        minute = (f"0{event.when.minute}" if event.when.minute in range(0, 10) else str(event.when.minute)) # Place a zero in front of single digit numbers (12:05 became 12:5, now it's still  12:05)
        delay_hours = event.when.hour - now.hour
        delay_minutes = event.when.minute - now.minute
        delay_minutes_string = (f"0{delay_minutes}" if delay_minutes in range(0, 10) else str(delay_minutes)) # Place a zero in front of single digit numbers (12:05 became 12:5, now it's still  12:05)
        
        if delay_hours > 0:
            delay = f"{delay_hours}h{delay_minutes_string}min"
        else:
            delay = f"{delay_minutes_string}min"

        s += f'\n{EVENT_BULLETPOINT} {event.when.hour}:{minute} - *{event.title}*\n(tra {delay})\n\n'
        s += f'"_{event.description}_"\n\n──────────────────────────\n'
    
    s += '\n⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️'

    return s


def craft_whole_day_events_notification_text(today_from_10_to_midnight_events : list[DayEvent], tomorrow_from_midnight_to_10 : list[DayEvent]) -> str:
    # Validation
    if not isinstance(today_from_10_to_midnight_events, list):
        err = f"today_from_10_to_midnight_events must be a list, not {type(today_from_10_to_midnight_events)}"
        scheduler_logger.error(err)
        print(err)
        return
        # raise TypeError(err)

    len_today_from_10_to_midnight_events = len(today_from_10_to_midnight_events)
    len_tomorrow_from_midnight_to_10 = len(tomorrow_from_midnight_to_10)

    # Logic
    if len_today_from_10_to_midnight_events + len_tomorrow_from_midnight_to_10 == 0:
        s = "*Buongiorno!* 💜💫\n\n🍻 Buone notizie, oggi *giornata libera*! 🍻\n      (include fino alle 10:00 di domani)\n\n🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
        return s
    
    elif len_today_from_10_to_midnight_events + len_tomorrow_from_midnight_to_10 == 1:
        s = "*Buongiorno!* 💜💫\nQuesto è l'evento della giornata di oggi (include fino alle 10:00 di domani).\n\n⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\n\n──────────────────────────\n"
    else:
        s = "*Buongiorno!* 💜💫\nQuesti sono gli eventi della giornata di oggi (include fino alle 10:00 di domani).\n\n⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\n\n──────────────────────────\n"

    EVENT_BULLETPOINT = '📝'

    # Craft string for events from today 10:00 AM to midnight
    for event in today_from_10_to_midnight_events:
        minute = (f"0{event.when.minute}" if event.when.minute in range(0, 10) else str(event.when.minute)) # Place a zero in front of single digit numbers (12:05 became 12:5, now it's still  12:05)
        s += f'\n{EVENT_BULLETPOINT} {event.when.hour}:{minute} - *{event.title}* \n\n'
        s += f'"_{event.description}_"\n\n──────────────────────────\n'
    
    # Craft string for events from tomorrow midnight to 10:00 AM
    if len_tomorrow_from_midnight_to_10 > 0:
        s += "\n\n⭐️⭐️⭐️⭐️  Domani  ⭐️⭐️⭐️⭐️\n\n"
        for event in tomorrow_from_midnight_to_10:
            minute = (f"0{event.when.minute}" if event.when.minute in range(0, 10) else str(event.when.minute)) # Place a zero in front of single digit numbers (12:05 became 12:5, now it's still  12:05)
            s += f'\n{EVENT_BULLETPOINT} {event.when.hour}:{minute} - *{event.title}* \n\n'
            s += f'"_{event.description}_"\n\n──────────────────────────\n'    

    
    s += '\n⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️'

    return s    


# ====================================
#            SEND MESSAGE
# ====================================

def make_bot_write(asyncio_loop, text) -> None:
    send_telegram_message(asyncio_loop=asyncio_loop, text=text)


def send_telegram_message(asyncio_loop, text):
    # Run the async message-sending part
    asyncio_loop.run_until_complete(ZeroCalendar_bot.send_message_in_ZeroCalendar_group_chat(text=text))








# ====================================
#            EXIT HANDLERS
# ====================================


def handle_exit_sigint():
    s = "-------!!!-------< SCHEDULER SHUTTING DOWN (ctrl+c) >-------!!!-------"
    scheduler_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)


def handle_exit_sigterm():
    s = "-------!!!-------< SCHEDULER SHUTTING DOWN (systemctl or kill) >-------!!!-------"
    scheduler_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)



if __name__ == '__main__':
    main()