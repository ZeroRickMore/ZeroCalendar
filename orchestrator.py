'''
Orchestrator that runs the app components.

Each component MUST have a main() function to start.
Fill the ALL_APPS = [] variable in this script with the name of the imported app component, the one in the "import" lines.
DO NOT PUT THE MAIN FLASK APP IN THE APP LIST! THAT IS STARTED BY ORCHESTRATOR ITSELF.
'''

import ZeroCalendar as flask_app
import ZeroCalendarBot.ZeroCalendarBot as telegram_bot_app
import ZeroCalendarBot.Scheduler.scheduler as scheduler_app
import threading
from threading import Thread
from loggers import orchestrator_logger
# Log process death
import signal
from sys import exit
import yaml
    
def load_settings() -> dict:
    with open("settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    return settings

# ====================================
#               VARIABLES
# ====================================

THREADS : list[Thread] = []

# ====================================
#          LOG PROCESS DEATH
# ====================================

def handle_exit_sigint(signum, frame):
    exit_orchestrator_cascade(type='sigint')
    s = "-------!!!-------< ORCHESTRATOR SHUTTING DOWN (ctrl+c) >-------!!!-------"
    orchestrator_logger.warning(s)
    print(s)
    exit(0)

def handle_exit_sigterm(signum, frame):
    exit_orchestrator_cascade(type='sigterm')
    s = "-------!!!-------< ORCHESTRATOR SHUTTING DOWN (systemctl or kill) >-------!!!-------"
    orchestrator_logger.warning(s)
    print(s)
    exit(0)

def exit_orchestrator_cascade(type : str):
    if type not in ['sigint', 'sigterm']:
        raise ValueError(f"type should be ['sigint', 'sigterm'], not {type}")
    
    match type:
        case 'sigint':
            for app_script in ALL_APPS:
                app_script.handle_exit_sigint()
            flask_app.handle_exit_sigint()

        case 'sigterm':
            for app_script in ALL_APPS:
                app_script.handle_exit_sigterm()
            flask_app.handle_exit_sigterm()

    
    # exit() should NOT go here!

def exit_orchestrator_solo():
    s = "-------!!!-------< ORCHESTRATOR SHUTTING DOWN (script-forced) >-------!!!-------"
    orchestrator_logger.warning(s)
    print(s)
    exit(0)


# ====================================
#       CHECK APPS FOR FUNCTIONS
# ====================================

def check_app_functions(script):
    '''
    This is a sort of abstract class but for scripts.
    It just checks that the exit handlers are properly implemented.
    '''
    required_functions = ['main', 'handle_exit_sigint', 'handle_exit_sigterm']

    errors = ''

    # Check if the script has all required functions
    for func in required_functions:
        if not callable(getattr(script, func, None)):
            s = func
            errors += s + ','
    
    if errors == '': return None

    return f"Script [{script.__name__}] did not implement: [{errors[:-1]}]. "


# Attach the signal handler for process kill logging
signal.signal(signal.SIGINT, handle_exit_sigint)  # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit_sigterm) # kill command (includes systemctl stop)

def main():
    s = "-----------------< ORCHESTRATOR STARTED >-----------------"
    orchestrator_logger.info(s)
    print(s)

    settings = load_settings()

    global ALL_APPS, THREADS

    if settings['Orchestrator']['RUN_TELEGRAMBOT_ONLY']:
        s = "Running on RUN_TELEGRAMBOT_ONLY"
        orchestrator_logger.warning(s)
        print(s)
        telegram_bot_app.main(
            USE_PRIVATE_CHAT=settings['TelegramBot']['USE_PRIVATE_CHAT'],
            POLLING=settings['TelegramBot']['POLLING'],
            # KEEP_ACTIVE is false if polling, else it must be true. So, just be the opposite of polling.
            KEEP_ACTIVE=(not settings['TelegramBot']['POLLING'])
        )
        exit()

    # Check imports (Double loop is important to not start threads uselessly) (worst case scenario accounted)
    errors = ''
    for current_app_script in [flask_app, telegram_bot_app, scheduler_app]:
        result = check_app_functions(script=current_app_script)
        if result is not None:
            errors += result
    if errors != '':
        orchestrator_logger.critical(errors)
        print(errors)
        exit_orchestrator_solo()
    
    errors = None

    # Main app start
    flask_thread = threading.Thread(target=flask_app.main, kwargs={
        "DEBUG" : settings['Flask']['DEBUG'],
    }, daemon=True)
    flask_thread.start()
    THREADS.append(flask_thread)

    # TelegramBot app start
    tgbot_thread = threading.Thread(target=telegram_bot_app.main, kwargs={
        'USE_PRIVATE_CHAT' : settings['TelegramBot']['USE_PRIVATE_CHAT'],
        'POLLING' : settings['TelegramBot']['POLLING'],
    }, daemon=True)
    tgbot_thread.start()
    THREADS.append(tgbot_thread)

    # Scheduler app start
    scheduler_thread = threading.Thread(target=telegram_bot_app.main, kwargs={
        'RUN_ONLY_FIRST_MESSAGE' : settings['Scheduler']['RUN_ONLY_FIRST_MESSAGE'],
        'DO_NOT_SKIP_NIGHT' : settings['Scheduler']['DO_NOT_SKIP_NIGHT'],
        'WAIT_ONLY_1_MINUTE' : settings['Scheduler']['WAIT_ONLY_1_MINUTE']

    }, daemon=True)
    scheduler_thread.start()
    THREADS.append(scheduler_thread)    

    # Join the flask_app thread fully or partially. Depends on the interactivity level required.
    # Joining only Flask is enough, considering every kind of process kill 
    if settings['Orchestrator']['NEED_KEYBOARD_INTERRUPT']:
        while flask_thread.is_alive():
            flask_thread.join(timeout=0.5)  # Join with a timeout
    else:
        flask_thread.join()




if __name__ == '__main__':
    main()