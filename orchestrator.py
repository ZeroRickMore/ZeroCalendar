'''
Orchestrator that runs the app components.

Each component MUST have a main() function to start.
Fill the ALL_APPS = [] variable in this script with the name of the imported app component, the one in the "import" lines.
'''

import ZeroCalendar as flask_app
import ZeroCalendarBot.ZeroCalendarBot as telegram_bot_app
import ZeroCalendarBot.Scheduler.scheduler as scheduler_app
import threading
from threading import Thread
from loggers import orchestrator_logger
# Log process death
import signal
import sys
import asyncio

# Define the apps
ALL_APPS : list = [flask_app, telegram_bot_app, scheduler_app]
# Define the threads
THREADS : list[Thread] = []


# ====================================
#          LOG PROCESS DEATH
# ====================================

def handle_exit_sigint(signum, frame):
    print("YO")
    exit_orchestrator_cascade(type='sigint')
    s = "-------!!!-------< ORCHESTRATOR SHUTTING DOWN (ctrl+c) >-------!!!-------"
    orchestrator_logger.warning(s)
    print(s)
    sys.exit(0)

def handle_exit_sigterm(signum, frame):
    print("YE")
    exit_orchestrator_cascade(type='sigterm')
    s = "-------!!!-------< ORCHESTRATOR SHUTTING DOWN (systemctl or kill) >-------!!!-------"
    orchestrator_logger.warning(s)
    print(s)
    sys.exit(0)

def exit_orchestrator_cascade(type : str):
    if type not in ['sigint', 'sigterm']:
        raise ValueError(f"type should be ['sigint', 'sigterm'], not {type}")
    
    match type:
        case 'sigint':
            for app_script in ALL_APPS:
                app_script.handle_exit_sigint()
        case 'sigterm':
            for app_script in ALL_APPS:
                app_script.handle_exit_sigterm()

def exit_orchestrator_solo():
    s = "-------!!!-------< ORCHESTRATOR SHUTTING DOWN (script-forced) >-------!!!-------"
    orchestrator_logger.warning(s)
    print(s)
    sys.exit(0)


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
    global ALL_APPS, THREADS

    # Check imports (Double loop is important to not start threads uselessly) (worst case scenario accounted)
    errors = ''
    for current_app_script in ALL_APPS:
        result = check_app_functions(script=current_app_script)
        if result is not None:
            errors += result
    if errors != '':
        orchestrator_logger.critical(errors)
        print(errors)
        exit_orchestrator_solo()
    
    errors = None
    # Finally run the apps
    for current_app_script in ALL_APPS:
        thread = threading.Thread(target=current_app_script.main, daemon=True)
        thread.start()
        THREADS.append(thread)

    for thread in THREADS:
        break
        thread.join()

    while True:
        pass

if __name__ == '__main__':
    main()