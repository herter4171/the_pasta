import logging
import colorlog

class BaseHasLogs(object):
    __logger = None

    @property
    def _logger(self):
        return BaseHasLogs.__logger

    def __init__(self):
        if not BaseHasLogs.__logger:
            BaseHasLogs.__logger = logging.getLogger()
            BaseHasLogs.__logger.setLevel(logging.INFO) # Set the lowest level

            # Create a handler
            handler = colorlog.StreamHandler()

            # Create a formatter with color codes
            formatter = colorlog.ColoredFormatter(
                '%(cyan)s%(asctime)s: %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red,bg_white',
                }
            )

            # Set the formatter for the handler
            handler.setFormatter(formatter)

            # Add the handler to the logger
            BaseHasLogs.__logger.addHandler(handler)