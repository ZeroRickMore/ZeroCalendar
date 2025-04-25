import ZeroCalendarBot.ZeroCalendarBot as ZeroCalendar_bot
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from loggers import telegrambot_logger
from models import DayEvent
from datetime import datetime, timedelta
import time

# ====================================
#            SEND MESSAGE
# ====================================

def send_telegram_message(text):
    # Run the async message-sending part
    asyncio.run(ZeroCalendar_bot.send_message_in_ZeroCalendar_group_chat(text=text))

def make_bot_write(text) -> None:
    send_telegram_message(text=text)

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

def get_events_in_next_hour():
    pass

def get_next_events() -> list[DayEvent]:
    pass

def check_next_events() -> None:
    events = get_next_events()
    if len(events)>0:  
        s = craft_events_notification_text(events=events)
        make_bot_write(text=s)

# ====================================
#                WAIT
# ====================================

def wait_until_next_quarter():
    now = datetime.now()
    minutes_to_wait = 15 - (now.minute % 15)
    next_quarter = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_wait)
    delay = (next_quarter - now).total_seconds()
    telegrambot_logger.info(f"SCHEDULER -> Waiting {delay:.1f} seconds to align with {next_quarter.strftime('%H:%M')}")
    time.sleep(delay)

# ====================================
#            MAIN METHOD
# ====================================

def create_and_start_tgbot_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_next_events, 'interval', minutes=15)

    wait_until_next_quarter()

    scheduler.start()
    telegrambot_logger.info(f"=================< Telegram Bot Scheduler JUST STARTED >=================")
    return scheduler