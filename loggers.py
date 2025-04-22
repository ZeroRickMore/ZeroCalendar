import logging
from flask import request

# ====================================
#              LOGGERS
# ====================================

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.remote_addr = request.remote_addr if request else 'N/A'
        record.method = request.method if request else 'N/A'
        record.path = request.path if request else 'N/A'
        return super().format(record)

if __name__ != '__main__':
    formatter = RequestFormatter(
        '%(asctime)s - %(levelname)s - %(remote_addr)s - %(method)s %(path)s - %(message)s'
    )

    file_handler = logging.FileHandler('ZeroCalendar.log')
    file_handler.setFormatter(formatter)

    # Flask has too many info logs, I don't want that many...
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
    werkzeug_logger.addHandler(file_handler)

    database_logger = logging.getLogger('db')
    database_logger.setLevel(logging.INFO)
    database_logger.addHandler(file_handler)

    # This is not the correct logger for this message, but I will not create a different one just for this...
    database_logger.info("=================< SERVER JUST STARTED >=================")