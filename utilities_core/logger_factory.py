import logging
import os

from date_utilities import DateUtilities
class LoggerFactory:
    def logger_controller(self, loggingLevel, message):
        switcher = {
            "INFO": self.logger_info(message),
            "ERROR": self.logger_error(message),
            "WARNING": ''
        }
        print (switcher.get(loggingLevel, "Invalid channel"))
        return switcher.get(loggingLevel, "Invalid channel")

    @staticmethod
    def logger_info(message):
        logging.basicConfig(filename=str(os.environ.get('LOGGER_FILE'))+'/bank_transactions_'+DateUtilities().getTodayDate().strftime('%Y-%m-%d')+'.log',
                            format='%(asctime)s -%(levelname)s- %(message)s',
                            level=logging.INFO)
        logging.getLogger('sqlalchemy').setLevel(logging.INFO)
        return logging.info(message)

    @staticmethod
    def logger_error(message):
        logging.basicConfig(filename=str(os.environ.get('LOGGER_FILE'))+'/bank_transactions_'+DateUtilities().getTodayDate().strftime('%Y-%m-%d')+'.log',
                            format='%(asctime)s -%(levelname)s- %(message)s',
                            level=logging.ERROR)
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
        return logging.error(message)

    @staticmethod
    def logger_exception(message):
        logging.basicConfig(filename=str(os.environ.get('LOGGER_FILE'))+'/bank_transactions_'+DateUtilities().getTodayDate().strftime('%Y-%m-%d')+'.log',
                            format='%(asctime)s -%(levelname)s- %(message)s',
                            level=logging.ERROR)
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
        return logging.error(message, exc_info=True)
