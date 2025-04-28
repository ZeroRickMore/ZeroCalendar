import logging
from flask import request

# ====================================
#              LOGGERS
# ====================================

class MultiFormatter(logging.Formatter):
    def format(self, record):
        # Default values if not inside a request
        record.remote_addr = request.remote_addr if request else 'N/A'
        record.method = request.method if request else 'N/A'
        record.path = request.path if request else 'N/A'

        # Different format based on logger name
        if record.name == 'db':
            self._style._fmt = '%(asctime)s [DB] [%(levelname)s] ===> %(message)s'
        elif record.name == 'telegrambot':
            self._style._fmt = '%(asctime)s [TELEGRAM BOT] [%(levelname)s] ===> %(message)s'
        elif record.name == 'scheduler':
            self._style._fmt = '%(asctime)s [SCHEDULER] [%(levelname)s] ===> %(message)s'
        elif record.name == 'werkzeug':
            self._style._fmt = '%(asctime)s [WERKZEUG] [%(levelname)s] - %(remote_addr)s - %(method)s %(path)s ===> %(message)s'
        elif record.name == 'myflask':
            self._style._fmt = '%(asctime)s [FLASK] [%(levelname)s] - %(remote_addr)s - %(method)s %(path)s ===> %(message)s'
        elif record.name == 'orchestrator':
            self._style._fmt = '%(asctime)s [ORCHESTRATOR] [%(levelname)s] ===> %(message)s'
        return super().format(record)



if __name__ != '__main__':
    formatter = MultiFormatter()

    file_handler = logging.FileHandler('ZeroCalendar.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
    werkzeug_logger.addHandler(file_handler)

    myflask_logger = logging.getLogger('myflask')
    myflask_logger.setLevel(logging.INFO)
    myflask_logger.addHandler(file_handler)

    database_logger = logging.getLogger('db')
    database_logger.setLevel(logging.INFO)
    database_logger.addHandler(file_handler)

    telegrambot_logger = logging.getLogger('telegrambot')
    telegrambot_logger.setLevel(logging.INFO)
    telegrambot_logger.addHandler(file_handler)

    scheduler_logger = logging.getLogger('scheduler')
    scheduler_logger.setLevel(logging.INFO)
    scheduler_logger.addHandler(file_handler)

    orchestrator_logger = logging.getLogger('orchestrator')
    orchestrator_logger.setLevel(logging.INFO)
    orchestrator_logger.addHandler(file_handler)