import ZeroCalendarBot.ZeroCalendarBot as ZeroCalendar_bot
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from loggers import telegrambot_logger
from models import db, DayEvent
from datetime import datetime, timedelta
import time
from ZeroCalendar import app

# ====================================
#            SEND MESSAGE
# ====================================

def send_telegram_message(asyncio_loop, text):
    # Run the async message-sending part
    asyncio_loop.run_until_complete(ZeroCalendar_bot.send_message_in_ZeroCalendar_group_chat(text=text))

def make_bot_write(asyncio_loop, text) -> None:
    send_telegram_message(asyncio_loop=asyncio_loop, text=text)

# ====================================
#            CRAFT MESSAGE
# ====================================

def craft_events_notification_text(events : list[DayEvent]) -> str:
    # Validation
    if not isinstance(events, list):
        raise TypeError(f"events must be a list, not {type(events)}")
    if len(events)==0:
        raise ValueError(f"Why was this function called with no events? len(events)==0")
    
    # Logic
    if len(events)==1:
        s = 'Ciao! Ricordatevi di questo evento!\n'
    else:
        s = 'Ciao! Ricordatevi di questi eventi!\n'

    EVENT_BULLETPOINT = '📝'

    for event in events:
        s += f'\n{EVENT_BULLETPOINT} *{event.title} ({event.when.hour}:{event.when.minute})*\n'
        s += f'{event.description}\n'
    
    return s

# ====================================
#             GET EVENTS
# ====================================

def get_events_in_next_hour() -> list[DayEvent]:
    now = datetime.now()
    today = now.date()
    current_hour = now.time()
    one_hour_later = (now + timedelta(hours=1)).time()

    with app.app_context():
        events : list[DayEvent] = db.session.query(DayEvent).filter(
            DayEvent.deleted == False, 
            DayEvent.day == today,
            DayEvent.when >= current_hour,
            DayEvent.when <= one_hour_later
        ).order_by('when').all()
    
    return events


def get_next_events() -> list[DayEvent]:
    '''
    For future implementation.
    Currently, just do hour events!
    '''
    return get_events_in_next_hour()

    '''
    if (current_hour is around 10:00 AM or similar):
        send notification with all day events for recap
    then
        send usual notification of get_events_in_next_hour()
    '''

def check_next_events(asyncio_loop) -> None:
    events = get_next_events()
    if len(events)>0:  
        s = craft_events_notification_text(events=events)
        make_bot_write(asyncio_loop=asyncio_loop, text=s)

# ====================================
#                WAIT
# ====================================

def wait_until_next_quarter():
    now = datetime.now()

    multiple_to_align_with = 15

    minutes_to_wait = multiple_to_align_with - (now.minute % multiple_to_align_with)

    next_quarter = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_wait)
    delay = (next_quarter - now).total_seconds()
    s = f"SCHEDULER -> Waiting {delay/60:.2f} minutes to align with {next_quarter.strftime('%H:%M')}"
    telegrambot_logger.info(s)
    print(s)
    time.sleep(delay)

def sleep_through_the_night():
    now = datetime.now()
    night_start = now.replace(hour=21, minute=0, second=0, microsecond=0)
    wake_time = now.replace(hour=10, minute=0, second=0, microsecond=0)

    if now >= night_start:
        # If after 21:00, sleep until 10:00 AM *tomorrow*
        wake_time += timedelta(days=1)
        sleep_duration = (wake_time - now).total_seconds()
        s = f"Scheduler Sleeping for {sleep_duration/3600:.2f} hours until {wake_time.strftime('%H:%M')}. GOODNIGHT!"
        telegrambot_logger.info(s)
        print(s)
        time.sleep(sleep_duration)
    else: # TODO DEBUG
        print("It's not night yet — no need to sleep.") # TODO DEBUG


# ====================================
#            MAIN METHOD
# ====================================

def run():
    DEBUG = True

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    s = f"=================< Telegram Bot Scheduler JUST STARTED >================="
    telegrambot_logger.info(s)
    print(s)

    # If it's night time, don't wake everybody up yet
    if not DEBUG:
        sleep_through_the_night()

    while(True):
        # wait_until_next_quarter() # Align with quarter, so wait 15 minutes
        check_next_events(asyncio_loop=loop)       # Send the message